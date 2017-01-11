from __future__ import absolute_import

from celery import shared_task
from .models import ImageModel,TimelineModel
from pusher import Pusher
import os

pusher = Pusher.from_url(os.environ["PUSHER_URL"])

@shared_task
def echo(param):
    return 'The test task executed with argument "%s" ' % param

@shared_task
def add(x, y):
    return x + y\
               
@shared_task
def send_image_notification(username, image_pik):
    image_json = ImageModel.objects.get(pk=image_pik).toJSON()
    username = username
    pusher.trigger(username, u'new_image', image_json)
    return "Send notification to user: %s with image_id: %s" % (username, image_pik)

@shared_task
def save_on_timeline(user_obj, image_obj):
    obj, isCreated = TimelineModel.objects.get_or_create(
        image=image_obj,
        user=user_obj
    )
    obj.save()
    return "Save image %s to user %s 's timeline!" % (image_obj.image.url, user_obj.username)