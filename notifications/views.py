from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.core.paginator import Paginator

# 创建视图

@login_required
def notification_list(request):
    # 获取当前用户的所有通知，按时间倒序排列
    # Ottieni tutte le notifiche dell'utente ordinate per data decrescente
    notification_qs = Notification.objects.filter(recipient=request.user).order_by('-created_at')

    # 分页，每页显示5条通知
    # Paginazione: 5 notifiche per pagina
    paginator = Paginator(notification_qs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 渲染通知收件箱页面，传递分页对象
    # Renderizza la pagina inbox con le notifiche paginati
    return render(request, 'notifications/inbox.html', {
        'page_obj': page_obj,
    })


@login_required
def mark_as_read(request, pk):
    # 标记指定通知为已读，确保该通知属于当前用户
    # Segna una notifica come letta assicurandosi che appartenga all'utente
    notif = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notif.is_read = True
    notif.save()

    # 标记成功后重定向回通知列表
    # Dopo la modifica, reindirizza alla lista notifiche
    return redirect('notification-list')
