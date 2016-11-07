from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm

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
	return render(request, 'publish.html')

@login_required
def edit_subscription(request):
	return render(request, 'subscribe.html')

@login_required
def view_notifications(request):
	return render(request, 'notifications.html')