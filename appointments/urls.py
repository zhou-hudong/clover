

from django.urls import path
from . import views

urlpatterns = [
    path('', views.appointment_list, name='appointment-list'),
    path('create/', views.appointment_create, name='appointment-create'),
    path('confirm/<int:pk>/', views.appointment_confirm, name='appointment-confirm'),
    path('edit-confirm/<int:pk>/', views.appointment_edit_confirm, name='appointment-edit-confirm'),
    path('edit/<int:pk>/', views.appointment_edit, name='appointment-edit'),
    path('delete/<int:pk>/', views.appointment_delete, name='appointment-delete'),
    path('cancelled/', views.appointment_cancelled, name='appointment-cancelled'),
]