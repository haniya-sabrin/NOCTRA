from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Message


@login_required(login_url='/login/')
def inbox(request):
    users = User.objects.exclude(id=request.user.id).order_by('username')

    return render(request, 'messaging/inbox.html', {
        'users': users
    })


@login_required(login_url='/login/')
def chat(request, username):
    other_user = get_object_or_404(User, username=username)

    if other_user == request.user:
        return redirect('inbox')

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()

        if content and len(content) <= 2000:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content
            )

        return redirect('chat', username=other_user.username)

    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('created_at')

    # Mark messages received by the current user as read
    messages.filter(
        receiver=request.user,
        is_read=False
    ).update(is_read=True)

    return render(request, 'messaging/chat.html', {
        'other_user': other_user,
        'messages': messages
    })