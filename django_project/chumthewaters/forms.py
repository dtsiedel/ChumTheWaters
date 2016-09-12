#used to create classes for all of the forms (probably just one) that we will use in this project

from django import forms

class summonerForm(forms.Form):
	summ_name = forms.CharField(label="Enemy summoner name", max_length=100)


