from __future__ import absolute_import

from celery import shared_task
from .models import ImageModel
from pusher import Pusher

pusher = Pusher(
    app_id=u'274247',
    key=u'a0e7e26bf61d7b3849c4',
    secret=u'1ba3ccae49d5dccd28d6'
)
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
    return "Send notification to user: %s with image_id: %s" % username, image_pik