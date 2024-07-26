from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from meetings.models import Meeting

def welcome(request):
    return render(request, "website/welcome.html", {"meetings": Meeting.objects.all()})

def about(request):
    return render(request, 'website/about.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})