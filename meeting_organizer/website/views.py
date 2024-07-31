from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm  # Importowanie wbudowanego formularza rejestracyjnego Django
from users.forms import CustomUserCreationForm  # Importowanie niestandardowego formularza rejestracyjnego
from django.contrib.auth import login, authenticate
from users.models import Profile
from meetings.models import Meeting

def welcome(request):
    return render(request, "website/welcome.html", {"meetings": Meeting.objects.all()})

def about(request):
    return render(request, 'website/about.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Użyj nowego formularza
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)  # Tworzenie profilu po rejestracji
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('welcome')  # Przekierowanie na stronę powitalną lub inną stronę po zalogowaniu
    else:
        form = CustomUserCreationForm()  # Użyj nowego formularza
    return render(request, 'registration/register.html', {'form': form})


