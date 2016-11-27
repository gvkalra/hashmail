from django.db import models
from cloudinary.models import CloudinaryField
from django.utils import timezone as timezone


class HashTagModel(models.Model):
    tag = models.CharField(max_length=30, unique=True)
    
    def __str__(self):
        return self.tag


class ImageModel(models.Model):
    image = CloudinaryField('image')
    tags = models.ManyToManyField(HashTagModel)
    date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=timezone.now(), null=True)
    
    
    
    #
    #  publish() will be used when the photo is sent to Rabbit MQ
    #
    
    def publish(self):
        self.published_date = timezone.now()
        
    def __unicode__(self):
        try:
            public_id = self.image.public_id
        except AttributeError:
            public_id = ''
        return "Photo <%s:%s>" % (self.title, public_id)

    def __str__(self):
        return "%s - %s",self.image.public_id, self.tags

"""
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    images = models.ManyToManyField(ImageModel)
    tags = models.ManyToManyField(HashTagModel)
"""
