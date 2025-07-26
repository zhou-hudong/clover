import random
from datetime import datetime, date, timedelta, time

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import AppointmentForm
from .models import Appointment
from users.models import Profile
from services.models import Service

from notifications.models import Notification

from django.core.paginator import Paginator


@login_required
def appointment_list(request):
    # 1. 解析 ?date=YYYY-MM-DD 参数，或默认为今天
    # 1. Analizza il parametro ?date=YYYY-MM-DD, o usa oggi come default
    date_str = request.GET.get('date')
    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else date.today()
    except (ValueError, TypeError):
        selected_date = date.today()

    # 2. 根据身份和日期筛选预约：
    # 2. Filtra gli appuntamenti in base al ruolo e alla data selezionata:
    if getattr(request.user, 'profile', None) and request.user.profile.is_barber:
        appts = Appointment.objects.filter(barber=request.user, date=selected_date)
    else:
        appts = Appointment.objects.filter(client=request.user, date=selected_date)

    # 3. 按时间升序排序
    # 3. Ordina per orario in ordine crescente
    appts = appts.order_by('time')

    paginator = Paginator(appts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'appointments/list.html', {
        'page_obj': page_obj,
        'selected_date': selected_date,
    })


@login_required
def appointment_create(request):
    # 理发师不允许自己预约
    # I barbieri non possono prenotare per se stessi
    if getattr(request.user, 'profile', None) and request.user.profile.is_barber:
        return redirect('home')

    if request.method == 'POST':
        form = AppointmentForm(request.POST, user=request.user)
        if form.is_valid():
            appt = form.save(commit=False)
            appt.client = request.user

            # 手动选择理发师优先，否则随机分配
            # Se il cliente ha scelto un barbiere, usalo; altrimenti assegnalo casualmente
            chosen = form.cleaned_data.get('barber')
            if chosen:
                appt.barber = chosen
            else:
                barber_ids = Profile.objects.filter(is_barber=True) \
                                             .values_list('user_id', flat=True)
                appt.barber_id = random.choice(list(barber_ids))

            # 检查预约时间冲突
            # Controlla se il barbiere ha già un appuntamento in questo slot
            if Appointment.objects.filter(
                    barber=appt.barber,
                    date=appt.date,
                    time=appt.time
                ).exists():
                service_obj = appt.service
                duration = service_obj.duration
                suggestions = get_next_slots(appt.barber, duration)
                return render(request, 'appointments/suggestions.html', {
                    'form': form,
                    'suggestions': suggestions,
                    'barber': appt.barber,
                })
            # 无冲突，保存预约
            # Nessun conflitto, salva l'appuntamento
            appt.save()

            # 创建通知给客户
            # Crea notifica per il cliente
            Notification.objects.create(
                recipient=request.user,
                message=f'Hai fissato con successo un appuntamento il giorno {appt.date} alle ore {appt.time} con {appt.barber.username}.'
            )

            # 创建通知给理发师
            # Crea notifica per il barbiere
            Notification.objects.create(
                recipient=appt.barber,
                message=f'{request.user.username} ho fissato un appuntamento con te il giorno {appt.date} alle ore {appt.time}.'
            )

            return redirect('appointment-confirm', pk=appt.pk)
    else:
        form = AppointmentForm(user=request.user)

    return render(request, 'appointments/create.html', {'form': form})


@login_required
def appointment_confirm(request, pk):
    appt = get_object_or_404(Appointment, pk=pk, client=request.user)
    return render(request, 'appointments/confirm.html', {'appt': appt})


@login_required
def appointment_edit(request, pk):
    appt = get_object_or_404(Appointment, pk=pk, client=request.user)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, user=request.user, instance=appt)
        if form.is_valid():
            new_appt = form.save(commit=False)
            new_appt.client = request.user

            # 手动或随机分配理发师
            # Barbiere scelto manualmente o assegnato casualmente
            chosen = form.cleaned_data.get('barber')
            if chosen:
                new_appt.barber = chosen
            else:
                barber_ids = Profile.objects.filter(is_barber=True) \
                                             .values_list('user_id', flat=True)
                new_appt.barber_id = random.choice(list(barber_ids))

            # 检查冲突，排除当前编辑的预约
            # Controlla conflitti escludendo l'appuntamento corrente
            if Appointment.objects.filter(
                    barber=new_appt.barber,
                    date=new_appt.date,
                    time=new_appt.time
                ).exclude(pk=pk).exists():
                    service_obj = new_appt.service
                    duration = service_obj.duration
                    suggestions = get_next_slots(new_appt.barber, duration)
                    return render(request, 'appointments/suggestions.html', {
                        'form': form,
                        'suggestions': suggestions,
                        'barber': new_appt.barber,
                    })
            else:
                new_appt.save()

                # 通知客户更新
                # Notifica il cliente dell'aggiornamento
                Notification.objects.create(
                    recipient=request.user,
                    message=f'Hai aggiornato il tuo appuntamento a {new_appt.date} alle {new_appt.time} con {new_appt.barber.username}.'
                )

                # 通知理发师更新
                # Notifica il barbiere dell'aggiornamento
                Notification.objects.create(
                    recipient=new_appt.barber,
                    message=f'{request.user.username} hanno aggiornato il loro appuntamento con te per {new_appt.date} alle {new_appt.time}.'
                )

                return redirect('appointment-edit-confirm', pk=new_appt.pk)
    else:
        form = AppointmentForm(user=request.user, instance=appt)

    return render(request, 'appointments/create.html', {'form': form})


@login_required
def appointment_edit_confirm(request, pk):
    appt = get_object_or_404(Appointment, pk=pk, client=request.user)
    return render(request, 'appointments/edit_confirm.html', {'appt': appt})


@login_required
def appointment_delete(request, pk):
    appt = get_object_or_404(Appointment, pk=pk, client=request.user)
    if request.method == 'POST':
        appt.delete()

        # 通知用户取消
        # Notifica il cliente della cancellazione
        Notification.objects.create(
            recipient=request.user,
            message=f'Hai annullato il tuo appuntamento del {appt.date} alle {appt.time} con {appt.barber.username}.'
        )

        # 通知理发师取消
        # Notifica il barbiere della cancellazione
        Notification.objects.create(
            recipient=appt.barber,
            message=f'{request.user.username} hanno annullato appuntamento con te il {appt.date} alle {appt.time}.'
        )

        return redirect('appointment-cancelled')
    return render(request, 'appointments/delete_confirm.html', {'appt': appt})


@login_required
def appointment_cancelled(request):
    return render(request, 'appointments/cancelled.html')


def get_next_slots(barber, service_duration, days_ahead=7, max_slots=3):
    """
    查找 barber 在未来 days_ahead 天内的空闲时段，每 slot 为 service_duration。
    返回 [(date, time), ...]，最多 max_slots 个。

    Trova gli slot liberi del barbiere nei prossimi giorni (days_ahead),
    ogni slot dura service_duration. Restituisce una lista di tuple (data, ora),
    fino a max_slots elementi.
    """
    slots = []
    start_date = date.today()
    # 生成时间候选列表 09:00–17:40，每20分钟
    # Crea lista di orari da 09:00 a 17:40 con intervalli di 20 minuti
    times = [time(h, m) for h in range(9, 18) for m in (0,20,40)]
    for day_offset in range(days_ahead):
        d = start_date + timedelta(days=day_offset)
        for t in times:
            if len(slots) >= max_slots:
                return slots
            # 跳过今天已经过去的时段
            # Salta gli orari già passati oggi
            if d == date.today() and t <= datetime.now().time():
                continue
            exists = Appointment.objects.filter(barber=barber, date=d, time=t).exists()
            if not exists:
                slots.append((d, t))
    return slots
