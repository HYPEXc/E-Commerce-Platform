from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(models.Model):
    clerk_id = models.CharField(max_length=255, unique=True)  # ID from Clerk
    email = models.EmailField(unique=True)  # Email for user identification
    username = models.CharField(max_length=150, unique=True)  # Optional, for user display
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Optional phone number
    date_joined = models.DateTimeField(auto_now_add=True)  # Timestamp of when the user joined
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True,
                                        null=True)  # Optional profile picture
    bio = models.TextField(blank=True, null=True)  # Optional bio for the user

    def __str__(self):
        return self.username or self.email  # Display username or email
