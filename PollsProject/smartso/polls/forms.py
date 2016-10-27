from django import forms
from django.forms import ModelForm
from .models import Question,Choice
from django.forms import modelformset_factory

class PollsForm(forms.ModelForm):
	class Meta:
		model=Question
		fields=['question_text']

	#Custom validator below for email:	#access other fields like clean_xyz
	# def clean_email(self):
	# 	email= self.cleaned_data.get('email')
	# 	email_base,provider = email.split('@')
	# 	domain,extension= provider.split('.')
		
	# 	if not extension=="edu":
	# 		raise forms.ValidationError("Please use a .edu email address")
	# 	return email
	# def clean_FullName(self):
	# 	full_name=self.cleaned_data.get('full_name')
	# 	return full_name
class ChoiceForm(forms.ModelForm):
	class Meta:
		model=Choice
		fields='__all__'
		exclude=['votes']
		