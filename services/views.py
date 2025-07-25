from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Service
from .forms import ServiceForm, ServiceFilterForm
from users.models import Profile
from datetime import timedelta
from django.core.paginator import Paginator


def service_list(request):
    # 服务列表页视图，支持筛选和分页
    # Vista dell'elenco dei servizi con filtro e paginazione
    form = ServiceFilterForm(request.GET or None)
    qs = Service.objects.all()

    if form.is_valid():
        cd = form.cleaned_data
        # 关键字搜索
        # Ricerca per parola chiave
        if cd.get('q'):
            qs = qs.filter(
                name__icontains=cd['q']
            ) | qs.filter(
                description__icontains=cd['q']
            )
        # 价格区间筛选
        # Filtro per intervallo di prezzo
        if cd.get('min_price') is not None:
            qs = qs.filter(price__gte=cd['min_price'])
        if cd.get('max_price') is not None:
            qs = qs.filter(price__lte=cd['max_price'])
        # 按时长筛选
        # Filtro per durata (in minuti)
        if cd.get('duration_minutes') is not None:
            td = timedelta(minutes=cd['duration_minutes'])
            qs = qs.filter(duration=td)

    services = qs.order_by('price')  # 默认按价格排序
    # Ordina per prezzo (default)

    # 分页，每页显示 5 项
    # Paginazione: 5 elementi per pagina
    paginator = Paginator(services, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'services/list.html', {
        'page_obj': page_obj,
        'filter_form': form,
    })


@login_required
def service_create(request):
    # 创建服务视图（理发师权限）
    # Vista per creare un nuovo servizio (solo barbiere)
    profile = Profile.objects.get(user=request.user)
    if not profile or not profile.is_barber:
        # 非理发师重定向回服务列表页
        # Se non è barbiere, reindirizza alla lista
        return redirect('service-list')

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.created_by = request.user
            service.save()
            # 创建成功后跳转确认页
            # Dopo creazione, mostra pagina di conferma
            return render(request, 'services/create_confirm.html', {
                'service': service,
                'action': 'created'
            })
    else:
        form = ServiceForm()
    return render(request, 'services/create.html', {'form': form})


@login_required
def service_edit(request, pk):
    # 编辑服务视图（只能编辑自己创建的）
    # Vista per modificare un servizio (solo proprio)
    service = get_object_or_404(Service, pk=pk)
    if request.user != service.created_by:
        return redirect('service-list')

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            # 编辑成功跳转确认页
            # Dopo modifica, mostra pagina di conferma
            return render(request, 'services/edit_confirm.html', {
                'service': service,
                'action': 'updated'
            })
    else:
        form = ServiceForm(instance=service)
    return render(request, 'services/edit.html', {'form': form})


@login_required
def service_delete(request, pk):
    # 删除服务视图（只能删除自己创建的）
    # Vista per eliminare un servizio (solo proprio)
    service = get_object_or_404(Service, pk=pk)
    if request.user != service.created_by:
        return redirect('service-list')

    if request.method == 'POST':
        # 保存被删除对象用于显示
        # Salva l'oggetto eliminato per mostrarlo nella conferma
        deleted_service = service
        service.delete()
        return render(request, 'services/delete_confirm.html', {
            'service': deleted_service,
            'action': 'deleted'
        })

    # 第一次访问删除页面时展示确认信息
    # Mostra conferma prima di eliminare
    return render(request, 'services/delete_confirm.html', {
        'service': service,
        'action': 'confirm'
    })


def homepage(request):
    """
    Same as service_list but renders home.html.
    Visible to all users.

    与 service_list 功能相同，只是用于首页显示，所有用户都可见。
    Stessa logica di service_list, ma visibile a tutti nella home page.
    """
    form = ServiceFilterForm(request.GET or None)
    qs = Service.objects.all()

    if form.is_valid():
        cd = form.cleaned_data
        if cd.get('q'):
            qs = qs.filter(name__icontains=cd['q']) | qs.filter(description__icontains=cd['q'])
        if cd.get('min_price') is not None:
            qs = qs.filter(price__gte=cd['min_price'])
        if cd.get('max_price') is not None:
            qs = qs.filter(price__lte=cd['max_price'])
        if cd.get('duration_minutes') is not None:
            qs = qs.filter(duration=timedelta(minutes=cd['duration_minutes']))

    services = qs.order_by('price')

    # 添加分页，每页显示 5 条
    # Paginazione: 5 elementi per pagina
    paginator = Paginator(services, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {
        'services': page_obj,
        'filter_form': form,
    })


