
from django import forms
from datetime import date, time, datetime
from .models import Appointment
from users.models import Profile
from django.contrib.auth.models import User

class AppointmentForm(forms.ModelForm):
    # 日期字段：禁选过去日期
    # Campo data: non permette selezionare date passate
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date', 'min': date.today().isoformat()}
        )
    )

    # 时间字段：每20分钟一个时间选项，从09:00到17:40
    # Campo orario: scelte ogni 20 minuti dalle 09:00 alle 17:40
    TIME_CHOICES = [
        (time(h, m), f"{h:02d}:{m:02d}")
        for h in range(9, 18)
        for m in (0, 20, 40)
    ]
    time = forms.ChoiceField(choices=TIME_CHOICES)

    # 理发师字段，选填，初始为空，动态赋值为所有 is_barber=True 的用户
    # Campo barbiere, opzionale, queryset impostato dinamicamente nel __init__
    barber = forms.ModelChoiceField(
        queryset=User.objects.none(),  # 初始空
        required=False,
        empty_label="(Assegnato casualmente)",
        label="Seleziona il personale (facoltativo)"
    )

    class Meta:
        model = Appointment
        fields = ['service', 'date', 'time', 'barber']
        labels = {
            'service': 'Servizio',
            'date': 'Data',
            'time': 'Orario',
        }

    def __init__(self, *args, **kwargs):
        # 提取传入的 user 对象
        # Estrae l'utente passato come argomento
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # 设置 barber queryset 为所有 is_barber=True 的用户
        # Imposta il queryset di barbiere solo per utenti con is_barber=True
        if user:
            barber_ids = Profile.objects.filter(is_barber=True).values_list('user_id', flat=True)
            self.fields['barber'].queryset = User.objects.filter(id__in=barber_ids)

    def clean(self):
        cleaned = super().clean()
        appt_date = cleaned.get('date')
        appt_time = cleaned.get('time')

        # 如果时间是字符串格式，尝试转换为 time 对象
        # Se appt_time è stringa, prova a convertirla in oggetto time
        if isinstance(appt_time, str):
            try:
                # 解析 "HH:MM" 或 "HH:MM:SS" 格式
                # Parsing formato "HH:MM" o "HH:MM:SS"
                appt_time = time.fromisoformat(appt_time)
            except ValueError:
                # 如果解析失败，使用 datetime.strptime 解析
                # Se fallisce, usa datetime.strptime per il parsing
                appt_time = datetime.strptime(appt_time, "%H:%M").time()
            cleaned['time'] = appt_time

        # 禁止预约当天的已过时间段
        # Non permette di prenotare orari passati nella giornata odierna
        if appt_date == date.today() and appt_time < datetime.now().time():
            self.add_error('time', 'Non è possibile aggiungere un orario passato oggi.')

        return cleaned


