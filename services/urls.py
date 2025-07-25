


from django.urls import path
from . import views

urlpatterns = [
    path('', views.service_list, name='service-list'),
    path('create/', views.service_create, name='service-create'),
    path('edit/<int:pk>/', views.service_edit, name='service-edit'),
    path('delete/<int:pk>/', views.service_delete, name='service-delete'),
]
