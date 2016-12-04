from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User as UserModel
from django.utils import timezone as timezone



class HashTagModel(models.Model):
    tag = models.CharField(max_length=30, unique=True)
    hashtag_subscription = models.ManyToManyField(UserModel)
    def __str__(self):
        return self.tag


class ImageModel(models.Model):
    image = CloudinaryField('image')
    image_tags = models.ManyToManyField(HashTagModel)
    image_author = models.ManyToManyField(UserModel)
    date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=timezone.now(), null=True)
    
    #
    #  publish() will be used when the photo is sent to Rabbit MQ
    #
    
    def publish(self):
        self.published_date = timezone.now()
        
    def notify_subscribed_users(self):
        hashtags = self.image_tags.values_list('pk', flat=True)
        return ""
     
    def toJSON(self):
        cloudinary_url = "https://res.cloudinary.com/hyiclya8s/image/upload/w_400,h_300/%s" % self.image.url.split("/")[-1]
        image_tags = " ".join(self.image_tags.values_list('tag', flat=True))
        image_author = "%s" % self.image_author.values_list('username', flat=True)[0]
        date = self.date.strftime('%A, %B %d %Y at %H:%M')
        import simplejson
        #return simplejson.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))
        return simplejson.dumps(dict(url = cloudinary_url,
                    hashtags=image_tags,
                    author=image_author,
                    published_date=date))
