from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)  # 加密密码 / Imposta la password (criptata)
            user.save()
            is_barber = form.cleaned_data['is_barber', False]  # 是否理发师字段 / Campo "È un barbiere"
            Profile.objects.create(user=user, is_barber=is_barber)  # 创建用户档案 / Crea il profilo utente
            login(request, user)  # 注册后自动登录 / Login automatico dopo la registrazione
            return redirect('home')  # 跳转主页 / Reindirizza alla home page
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)  # 验证用户名和密码 / Autentica username e password
        if user:
            login(request, user)  # 登录用户 / Effettua il login
            return redirect('home')  # 登录后跳转主页 / Reindirizza alla home page dopo il login
        else:
            return render(request, 'users/login.html',
                          {'error': 'Invalid credentials'})  # 登录失败提示 / Messaggio di errore login
    return render(request, 'users/login.html')

@login_required
def profile_view(request):
    # 获取当前用户的 Profile
    # Ottieni il profilo dell'utente corrente
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save() # 保存用户资料 / Salva il profilo
            return render(request, 'users/profile_confirm.html', {'field': 'Profile'})  # 保存后刷新本页
    else:
        form = ProfileForm(instance=profile, user=request.user)

    return render(request, 'users/profile.html', {'form': form})


@login_required
def profile_detail(request, user_id):
    """
    供理发师查看客户资料的只读页面。
    Pagina di sola lettura del profilo, per i barbieri che visualizzano i clienti.
    """
    user_obj = get_object_or_404(User, pk=user_id)  # 根据 user_id 获取用户 / Ottieni utente tramite user_id
    profile = user_obj.profile  # 获取对应的 Profile / Ottieni il profilo corrispondente
    return render(request, 'users/profile_detail.html', {
        'profile_user': user_obj,
        'profile': profile,
    })
