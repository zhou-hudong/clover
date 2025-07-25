from django.db import models
from django.contrib.auth.models import User
from services.models import Service

# Create your models here.

class Appointment(models.Model):
    client = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='client_appointments'
    )
    barber = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='barber_appointments'
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        #unique_together = ('barber', 'date', 'time')
        ordering = ['-date', '-time']

    def __str__(self):
        # 预约的字符串表示
        # Rappresentazione stringa dell'appuntamento
        return f"{self.client.username} → {self.barber.username} on {self.date} at {self.time}"
