from django.db import models
from django.contrib.auth.models import User

class HashTagModel(models.Model):
	tag = models.CharField(max_length=30, unique=True)

	def __str__(self):
		return self.tag

class ImageModel(models.Model):
	url = models.URLField(max_length=200)
	date = models.DateTimeField(auto_now_add=True)
	tags = models.ManyToManyField(HashTagModel)

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	images = models.ManyToManyField(ImageModel)
	tags = models.ManyToManyField(HashTagModel)