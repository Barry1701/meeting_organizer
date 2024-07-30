from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from meetings.models import Meeting

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    # Fetch meetings created by the logged-in user
    user_meetings = Meeting.objects.filter(created_by=request.user)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_meetings': user_meetings
    }

    return render(request, 'users/profile.html', context)

