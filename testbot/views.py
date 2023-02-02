from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Testbot
from .serializers import TestbotModelSerializer
from .forms import TestbotForm
import numpy as np
import random
import json
from django.utils import timezone
import nltk
import torch
import torch.nn as nn
nltk.download('punkt')
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()
# Create your views here.

MODELS_PATH = './models/'

class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size) 
        self.l2 = nn.Linear(hidden_size, hidden_size) 
        self.l3 = nn.Linear(hidden_size, num_classes)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        # no activation and no softmax at the end
        return out

class TestbotAPIView(APIView):

    def get(self, request):
        testbot = Testbot.objects.all()
        serializer = TestbotModelSerializer(testbot, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = TestbotModelSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = 201)
        return Response(serializer.errors, status = 400)

    def testbot(request):
        testbot_form = TestbotForm()
        return render(request, template_name='pages/testbot.html', context={'testbot_form':testbot_form})


def bag_of_words(tokenized_sentence, words):
    """
    return bag of words array:
    1 for each known word that exists in the sentence, 0 otherwise
    example:
    sentence = ["hello", "how", "are", "you"]
    words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
    bog   = [  0 ,    1 ,    0 ,   1 ,    0 ,    0 ,      0]
    """
    # stem each word
    sentence_words = [stemmer.stem(str(word).lower()) for word in tokenized_sentence]
    # initialize bag with 0 for each word
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words: 
            bag[idx] = 1

    return bag    


def convo(request):

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    with open(MODELS_PATH+'testbot.json', 'r') as json_data:
        intents = json.load(json_data)

    FILE = MODELS_PATH+"model_data.pth"
    data = torch.load(FILE,map_location=device)

    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]
    all_words = data['all_words']
    tags = data['tags']
    model_state = data["model_state"]

    model = NeuralNet(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()

    if request.method == 'POST':

            print("Enter form")

            sent_time = timezone.now

            testbot_form = TestbotForm(request.POST)

            if testbot_form.is_valid():

                sentence = request.POST['input_field']

                sentence_token = nltk.word_tokenize(sentence)
                X = bag_of_words(sentence_token, all_words)
                X = X.reshape(1, X.shape[0])
                X = torch.from_numpy(X).to(device)

                output = model(X)
                _, predicted = torch.max(output, dim=1)

                tag = tags[predicted.item()]


                # bot_response = None
                probs = torch.softmax(output, dim=1)
                prob = probs[0][predicted.item()]
                if prob.item() > 0.75:
                    for intent in intents['intents']:
                        if tag == intent["tag"]:
                            bot_response = random.choice(intent['response'])
                            testbot_form = TestbotForm()
                            return render(request, template_name='pages/testbot.html', context={'testbot_form':testbot_form,'query_sentence':sentence, 'bot_response':bot_response,'sent_time':sent_time})
                else:
                    bot_response = 'I do not understand...'
                    testbot_form = TestbotForm()
                    return render(request, template_name='pages/testbot.html', context={'testbot_form':testbot_form,'query_sentence':sentence, 'bot_response':bot_response, 'response_time':timezone.now})

            else:
                 print(testbot_form.errors.as_data()) # here you print errors to terminal

    testbot_form = TestbotForm()
    return render(request, template_name='pages/testbot.html', context={'testbot_form':testbot_form})

