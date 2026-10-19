from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Like, Comment
from notifications.models import Notification


@login_required(login_url='/login/')
def feed(request):
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()

        if content:
            Post.objects.create(
                author=request.user,
                content=content
            )

        return redirect('feed')

    posts = Post.objects.all().order_by('-created_at')

    for post in posts:
        post.user_has_liked = post.likes.filter(
            user=request.user
        ).exists()

    return render(
        request,
        'posts/feed.html',
        {'posts': posts}
    )


@login_required(login_url='/login/')
def like_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)

        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post
        )

        if created:
            if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    sender=request.user,
                    notification_type='like',
                    message=f'{request.user.username} liked your post.',
                    post_id=post.id
                )
        else:
            like.delete()

    return redirect('feed')


@login_required(login_url='/login/')
def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get('content', '').strip()

        if content and len(content) <= 1000:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )

            if post.author != request.user:
                notification = Notification.objects.create(
                    recipient=post.author,
                    sender=request.user,
                    notification_type='comment',
                    message=f'{request.user.username} commented on your post.',
                    post_id=post.id
                )

    return redirect('feed')


@login_required(login_url='/login/')
def delete_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(
            Comment,
            id=comment_id,
            author=request.user
        )

        comment.delete()

    return redirect('feed')