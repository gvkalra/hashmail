from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt  
from .forms import RegistrationForm, ImageDirectForm

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
def edit_subscription(request):
	return render(request, 'subscribe.html')

@login_required
def view_notifications(request):
	return render(request, 'notifications.html')

@login_required
@csrf_exempt
def publish_result(request):
    form = ImageDirectForm(request.POST)
    if form.is_valid():
        tags = form.cleaned_data['tags'].split(' ')
        image = form['image']

        for tag in tags:
            obj, created = HashTagModel.objects.get_or_create(tag=tag)

        #ret = dict(photo_id = form.instance.id)
    else:
        ret = dict(errors = form.errors)
    return HttpResponse("ok")#json.dumps(ret), content_type='application/json')