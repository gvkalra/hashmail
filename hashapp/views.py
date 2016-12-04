from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt  
from .forms import RegistrationForm, ImageDirectForm, SubscriptionForm
from django.core.exceptions import ObjectDoesNotExist

from cloudinary import CloudinaryImage
from cloudinary.forms import cl_init_js_callbacks
from .models import ImageModel, HashTagModel, TimelineModel

from django.http import HttpResponse
import json
import random
import cloudinary


def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # login & redirect
            new_user = authenticate(username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],)
            login(request, new_user)
            return HttpResponseRedirect('/')
    else:
        form = RegistrationForm()

    return render(request, 'registration/signup.html', {'form': form})

def view_index(request):
    try:
        img = random.choice(ImageModel.objects.all())
        url = "https://res.cloudinary.com/hootddo4i/image/upload/w_400,h_300/%s" % img.image.url.split("/")[-1]
        tags = " ".join(img.image_tags.values_list('tag', flat=True))
        date = img.date.strftime('%A, %B %d %Y at %H:%M')

        rand_image = {'url': url, 'published_date': date, 'hashtags': tags}
        return render(request, 'index.html',
            {'rand_image': rand_image})
    except:
        return render(request, 'index.html')

@login_required
def publish_image(request):
    context = dict(image_form = ImageDirectForm())
    cl_init_js_callbacks(context['image_form'], request)
    return render(request, 'publish.html', context)

@login_required
def add_subscription(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        subscription_form = SubscriptionForm(request.POST)
        # check whether it's valid:
        if subscription_form.is_valid():
            # process the data in form.cleaned_data as required
            tags = subscription_form.cleaned_data['tags'].split(' ')
            filter(None, tags)
            if len(tags) > 0:
                for tag in tags:
                    obj, created = HashTagModel.objects.get_or_create(tag=tag)
                    obj.hashtag_subscription.add(request.user)
                    obj.save()

    return HttpResponseRedirect('/subscribe')

@login_required
def remove_subscription(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        subscription_form = SubscriptionForm(request.POST)
        # check whether it's valid:
        if subscription_form.is_valid():
            # process the data in form.cleaned_data as required
            tags = subscription_form.cleaned_data['tags'].split(' ')
            filter(None, tags)
            if len(tags) > 0:
                for tag in tags:
                    try:
                        obj = HashTagModel.objects.get(tag=tag)
                        obj.hashtag_subscription.remove(request.user) # only unlink
                    except ObjectDoesNotExist:
                        pass

    return HttpResponseRedirect('/subscribe')

@login_required
def manage_subscription(request):

    subscription_form = SubscriptionForm()
    current_subscription = HashTagModel.objects.filter(hashtag_subscription=request.user)

    return render(request, 'subscribe.html',
                  {'subscription_form': subscription_form,
                   'current_subscription': current_subscription})

@login_required
def view_notifications(request):
    timeline_objects = TimelineModel.objects.filter(user=request.user)
    current_images = []

    for obj in timeline_objects:
        my_dictionary = {}
        tags = " ".join(obj.image.image_tags.values_list('tag', flat=True))
        date = obj.image.date.strftime('%A, %B %d %Y at %H:%M')
        url = "https://res.cloudinary.com/hootddo4i/image/upload/w_400,h_300/%s" % obj.image.image.url.split("/")[-1]
        my_dictionary.update({"date": date, "tags": tags, "url": url})       

        current_images.append(my_dictionary)
    return render(request, 'notifications.html',
        {'current_images': current_images})

@login_required
@csrf_exempt
def publish_result(request):
    form = ImageDirectForm(request.POST)
    cloudinary.forms.cl_init_js_callbacks(form, request)
    my_dictionary = {}

    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data
            tags = data['tags'].split(' ')
            filter(None, tags)
            image = data['image']
            if 'published' in request.POST: #request is coming from our form
                pass
            else:
                saved_image, is_new_image = ImageModel.objects.get_or_create(image=image)
                saved_image.image_author.add(request.user)
                #Saving tags and adding to the Image relationship
                if len(tags) > 0:
                    for tag in tags:
                        obj, created = HashTagModel.objects.get_or_create(tag=tag)
                        saved_image.image_tags.add(obj)
                        saved_image.save()
                saved_image.notify_subscribed_users()

            my_dictionary.update(dict(image=image))
            my_dictionary.update({"tags": tags})
        else:
            my_dictionary.update(dict(errors = form.errors))
        return render(request, 'published_photo.html', dictionary=my_dictionary)
