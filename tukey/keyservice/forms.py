from django import forms
from django.forms import ModelForm
from tukey.keyservice.models import Repository, Key

class ARKForm(forms.Form):
    ark_key = forms.CharField(max_length=2000, widget=forms.TextInput(attrs={'class' : 'span4'}))


class RepositoryForm(ModelForm):
	class Meta:
		model = Repository

class KeyForm(ModelForm):
	class Meta:
		model = Key
