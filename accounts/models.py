from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        default='profile_pictures/default.png',
        blank=True
    )

    bio = models.TextField(
        max_length=300,
        blank=True
    )
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"
