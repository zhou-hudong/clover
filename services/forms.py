

from django import forms
from .models import Service
from datetime import timedelta

class ServiceForm(forms.ModelForm):
    # 在原来基础上新增一个只读分钟数字段
    # Aggiunge un campo in minuti (sola lettura) basato sulla durata originale
    duration_minutes = forms.IntegerField(
        required=True,
        min_value=0,
        label="Duration (minutes)",
        help_text="Enter number of minutes, e.g. 40"
    )

    class Meta:
        model = Service
        fields = ['name', 'description', 'price', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 编辑模式时，把已有 duration 转到分钟字段
        # In modalità modifica, converte la durata esistente in minuti
        if self.instance and self.instance.duration:
            total_secs = self.instance.duration.total_seconds()
            self.initial['duration_minutes'] = int(total_secs // 60)

    def clean_duration_minutes(self):
        mins = self.cleaned_data['duration_minutes']
        # 验证：时长不能为负数
        # Validazione: la durata non può essere negativa
        if mins < 0:
            raise forms.ValidationError("Duration must be zero or positive.")
        return mins

    def save(self, commit=True):
        # 保存前把分钟数转成 timedelta 并赋值给实例的 duration
        # Prima del salvataggio, converte i minuti in timedelta e assegna a 'duration'
        mins = self.cleaned_data.pop('duration_minutes')
        self.instance.duration = timedelta(minutes=mins)
        return super().save(commit=commit)

class ServiceFilterForm(forms.Form):
    # 服务筛选表单 - 关键字、价格范围、时长
    # Modulo di filtro dei servizi: parola chiave, prezzo, durata
    q = forms.CharField(required=False, label="Keyword")
    min_price = forms.DecimalField(
        required=False, min_value=0, decimal_places=2, label="Min Price (€)"
    )
    max_price = forms.DecimalField(
        required=False, min_value=0, decimal_places=2, label="Max Price (€)"
    )
    duration_minutes = forms.IntegerField(
        required=False,
        min_value=0,
        label="Duration (minutes)",
        help_text="Enter number of minutes, e.g. 30"
    )

