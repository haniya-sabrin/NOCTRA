from django.shortcuts import render, redirect, get_object_or_404
from posts.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import Profile
from posts.models import Post, Follow
from notifications.models import Notification

def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        errors = []

        if not username or not email or not password1:
            errors.append("Please fill in all required fields.")

        if User.objects.filter(username=username).exists():
            errors.append("This username is already taken.")

        if password1 != password2:
            errors.append("Passwords do not match.")

        if len(password1) < 8:
            errors.append("Password must contain at least 8 characters.")

        if errors:
            return render(
                request,
                'register.html',
                {'errors': errors}
            )

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )

            login(request, user)
            return redirect('home')

        except IntegrityError:
            errors.append("Unable to create the account. Try another username.")
            return render(
                request,
                'register.html',
                {'errors': errors}
            )

    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        return render(
            request,
            'login.html',
            {'error': 'Invalid username or password.'}
        )

    return render(request, 'login.html')


def user_logout(request):
    if request.method == 'POST':
        logout(request)

    return redirect('home')
@login_required(login_url='/login/')
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        bio = request.POST.get('bio', '').strip()

        if len(bio) > 300:
            return render(request, 'edit_profile.html', {
                'profile': profile,
                'error': 'Bio must be 300 characters or fewer.'
            })

        profile.bio = bio

        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES['profile_picture']

        profile.save()
        return redirect('edit_profile')

    return render(request, 'edit_profile.html', {'profile': profile})
def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)

    profile, created = Profile.objects.get_or_create(
        user=profile_user
    )

    # Check whether the logged-in user follows this profile
    is_following = False

    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=profile_user
        ).exists()

    # Check whether the viewer is allowed to see posts
    can_view_posts = (
        not profile.is_private
        or (
            request.user.is_authenticated
            and request.user == profile_user
        )
        or is_following
    )

    # Show posts only if the account is public or access is allowed
    if can_view_posts:
        user_posts = Post.objects.filter(
            author=profile_user
        ).order_by('-created_at')
    else:
        user_posts = Post.objects.none()

    follower_count = Follow.objects.filter(
        following=profile_user
    ).count()

    following_count = Follow.objects.filter(
        follower=profile_user
    ).count()

    context = {
        'profile_user': profile_user,
        'profile': profile,
        'user_posts': user_posts,
        'post_count': Post.objects.filter(
            author=profile_user
        ).count(),
        'follower_count': follower_count,
        'following_count': following_count,
        'is_following': is_following,
        'can_view_posts': can_view_posts,
    }

    return render(request, 'user_profile.html', context)
@login_required(login_url='/login/')
def toggle_follow(request, username):
    if request.method != 'POST':
        return redirect('user_profile', username=username)

    target_user = get_object_or_404(User, username=username)

    if request.user == target_user:
        return redirect('user_profile', username=username)

    follow = Follow.objects.filter(
        follower=request.user,
        following=target_user
    )

    if follow.exists():
        follow.delete()
    else:
        Follow.objects.create(
            follower=request.user,
            following=target_user
        )

        Notification.objects.create(
            recipient=target_user,
            sender=request.user,
            notification_type='follow',
            message=f'{request.user.username} started following you.'
        )
    return redirect('user_profile', username=username)
@login_required(login_url='/login/')
def explore_users(request):
    users = User.objects.exclude(
        id=request.user.id
    ).order_by('username')

    for user in users:
        user.is_following = Follow.objects.filter(
            follower=request.user,
            following=user
        ).exists()

    return render(
        request,
        'explore.html',
        {'users': users}
    )
# PRIVACY SETTINGS
@login_required(login_url='/login/')
def privacy_settings(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':
        profile.is_private = (
            request.POST.get('is_private') == 'on'
        )
        profile.save()

        return redirect('privacy_settings')

    return render(
        request,
        'accounts/privacy_settings.html',
        {'profile': profile}
    )