from django import forms
from django.forms import ModelForm, Textarea
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ImageModel
from cloudinary.forms import CloudinaryJsFileField

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField(required=False)
	last_name = forms.CharField(required = False)

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')

	def save(self, commit=True):
		user = super(RegistrationForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']

		if commit:
			user.save()

		return user

class ImageDirectForm(forms.Form):
	class Meta:
		model = ImageModel
	image = CloudinaryJsFileField()
	tags = forms.CharField(required=True)

class SubscriptionForm(forms.Form):
	tags = forms.CharField(required=True)