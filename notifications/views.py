from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification


@login_required(login_url='/login/')
def notification_list(request):
    notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by('-created_at')

    notifications.filter(is_read=False).update(is_read=True)

    return render(request, 'notifications/notifications.html', {
    'notifications': notifications
})