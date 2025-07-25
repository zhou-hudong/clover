
from .models import Notification

def unread_notification_count(request):
    # 如果用户已登录，统计未读通知数量
    # Se l'utente è autenticato, conta il numero di notifiche non lette
    if request.user.is_authenticated:
        count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        # 将未读数量作为上下文变量返回，供模板使用
        # Restituisce il conteggio come variabile di contesto per i template
        return {'unread_notification_count': count}

    # 如果未登录，返回空上下文
    # Se non autenticato, restituisce contesto vuoto
    return {}
