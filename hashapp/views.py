from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm

def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = RegistrationForm()

    return render(request, 'registration/signup.html', {'form': form})

def view_index(request):
    return render(request, 'index.html')