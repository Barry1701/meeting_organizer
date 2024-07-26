from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from meetings.models import Meeting

def welcome(request):
    return render(request, "website/welcome.html", {"meetings": Meeting.objects.all()})

def about(request):
    return HttpResponse("I am a dedicated father of two with 15 years of experience in the security environment. Throughout my career, I have developed a strong foundation in maintaining safety and security, ensuring a secure environment for both people and property.Currently, I am expanding my skill set by completing a Full Stack Web Development course at the Code Institute. This new venture has ignited a deep passion for technology and coding within me. I am enthusiastic about combining my extensive experience in security with my newfound skills in web development to pursue innovative and dynamic opportunities in the tech industry")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})