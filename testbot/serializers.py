from rest_framework import serializers
from .models import Testbot

class TestbotModelSerializer(serializers.ModelSerializer):

    class Meta:

        model = Testbot

        # fields = ('__all__')