from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Meeting, Room
from .forms import MeetingForm

def detail(request, id):
    meeting = get_object_or_404(Meeting, pk=id)
    return render(request, "meetings/detail.html", {"meeting": meeting})

def rooms_list(request):
    return render(request, "meetings/rooms_list.html", {"rooms": Room.objects.all()})

@login_required
def new(request):
    if request.method == "POST":
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.created_by = request.user
            meeting.save()
            return redirect('welcome')
    else:
        form = MeetingForm()
    return render(request, "meetings/new.html", {"form": form})
