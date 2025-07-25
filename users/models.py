from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_barber = models.BooleanField(default=False)  # True 表示理发师
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"