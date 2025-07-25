from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to="services/")
    duration = models.DurationField(default=timedelta(minutes=30))
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name