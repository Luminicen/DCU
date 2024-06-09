from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from .forms import Registro

def index(request):
    return render(request, 'base.html')

def register(request):
    if request.method == 'POST':
        form = Registro(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # Load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = Registro()
    return render(request, 'registration/registerForm.html', {'form': form})

def analysis(request):
    return render(request, "analysis/analysis.html")

def results(request):
    return render(request, 'results/results.html')

def settings(request):
    return render(request, 'settings/settings.html')