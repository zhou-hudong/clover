


from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='notification-list'),
    path('read/<int:pk>/', views.mark_as_read, name='notification-read'),
]