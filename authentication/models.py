from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    supabase_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Profile"