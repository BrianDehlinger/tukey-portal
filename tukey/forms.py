from django import forms

class RegisterIdForm(forms.Form):
    method = forms.CharField()
    identifier = forms.CharField()
    username = forms.CharField()

