
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserRegisterForm(forms.ModelForm):
    # 用户注册表单，包含密码和是否理发师的字段
    # Modulo di registrazione utente, include password e campo per "sei un barbiere?"
    password = forms.CharField(widget=forms.PasswordInput)
    is_barber = forms.BooleanField(required=False, label="Are you a barber?")  # 是否理发师（可选）
    # Sei un barbiere? (opzionale)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # 注册需要的字段
        # Campi richiesti per la registrazione

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Email Address")
    is_barber = forms.BooleanField(required=False, label="I am a Barber")
    avatar = forms.ImageField(required=False, label="Avatar")
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':4}),
                                  required=False,
                                  label="Description")

    class Meta:
        model = Profile
        fields = ['is_barber', 'avatar', 'description']

    def __init__(self, *args, **kwargs):
        # 接收 user 实例，用于更新 User.email
        # Riceve istanza user per aggiornare User.email
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            # 初始化 email 和 description 字段默认值
            # Imposta valori iniziali per email e descrizione
            self.fields['email'].initial = self.user.email
            self.fields['description'].initial = self.instance.description

    def save(self, commit=True):
        profile = super().save(commit=False)
        # 更新 User.email 字段
        # Aggiorna campo User.email
        if self.user:
            self.user.email = self.cleaned_data['email']
            if commit:
                self.user.save()
        if commit:
            profile.save()
        return profile