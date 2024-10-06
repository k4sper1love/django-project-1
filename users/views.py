from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from users.forms import ProfileForm
from users.models import Follow, Profile


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Регистрация прошла успешно. Теперь вы можете войти.')
            Profile.objects.create(user=user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/registration.html', {"form": form})

@login_required
def get_profile(request, user_id=None):
    if user_id is None:
        profile = request.user.profile
        user = request.user
    else:
        user = get_object_or_404(User, id=user_id)
        try:
            profile = user.profile
        except Profile.DoesNotExist:
            profile = None

    followers_count = Follow.objects.filter(following=request.user).count()
    following_count = Follow.objects.filter(follower=request.user).count()

    return render(request, 'users/profile.html', {
        'profile': profile,
        'user': user,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': Follow.objects.filter(follower=request.user, following=user).exists(),
    })

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('get_profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'users/profile_form.html', {"form": form})

@login_required
def follow_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if user == request.user:
        return redirect('get_profile')

    Follow.objects.get_or_create(follower=request.user, following=user)
    return redirect('get_profile', user_id=user.id)

@login_required
def unfollow_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    Follow.objects.filter(follower=request.user, following=user).delete()
    return redirect('get_profile', user_id=user.id)