from django import forms


class TestbotForm(forms.Form):
    input_field = forms.CharField(max_length=255, widget=(forms.TextInput(attrs={'class':'form-control','placeholder':'Type a here...', 'class':'textarea'})))