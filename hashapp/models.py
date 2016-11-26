from django.db import models
# from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class HashTagModel(models.Model):
    tag = models.CharField(max_length=30, unique=True)
    
    def __str__(self):
        return self.tag


class ImageModel(models.Model):
    image = CloudinaryField('image')
    tags = models.ManyToManyField(HashTagModel)
    date = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        try:
            public_id = self.image.public_id
        except AttributeError:
            public_id = ''
        return "Photo <%s:%s>" % (self.title, public_id)


"""
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    images = models.ManyToManyField(ImageModel)
    tags = models.ManyToManyField(HashTagModel)
"""
