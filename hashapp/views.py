from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt  
from .forms import RegistrationForm, ImageDirectForm, SubscriptionForm

from cloudinary import CloudinaryImage
from cloudinary.forms import cl_init_js_callbacks
from .models import ImageModel, HashTagModel

from django.http import HttpResponse
import json

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
            # redirect to a new URL:
            return HttpResponseRedirect('/subscribe')

    # if a GET (or any other method) we'll create a blank form
    else:
        subscription_form = SubscriptionForm()

    return render(request, 'subscribe_add.html',
        {'subscription_form': subscription_form})

@login_required
def remove_subscription(request):
    pass

@login_required
def manage_subscription(request):
    return render(request, 'subscribe.html')

@login_required
def view_notifications(request):
    return render(request, 'notifications.html')

@login_required
@csrf_exempt
def publish_result(request):
    form = ImageDirectForm(request.POST)
    my_dictionary = {}
    if form.is_valid():
        data = form.cleaned_data
        tags = data['tags'].split(' ')
        filter(None, tags)
        image = data['image']
        saved_image, is_new_image = ImageModel.objects.get_or_create(image=image)
        saved_image.image_author.add(request.user)
        #Saving tags and adding to the Image relationship
        if len(tags) > 0:
            for tag in tags:
                obj, created = HashTagModel.objects.get_or_create(tag=tag)
                saved_image.image_tags.add(obj)
                saved_image.save()

        my_dictionary.update(dict(image=image))
        my_dictionary.update({"tags": tags})
    else:
        my_dictionary.update(dict(errors = form.errors))
    return render(request, 'published_photo.html', dictionary=my_dictionary)