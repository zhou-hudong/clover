from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        # Ordina le notifiche dalla più recente alla più vecchia
        ordering = ['-created_at']  # 最新通知排在前面

    def __str__(self):
        # 返回通知简短信息，方便后台显示
        # Rappresentazione stringa breve della notifica
        return f"To {self.recipient.username}: {self.message[:40]}..."
