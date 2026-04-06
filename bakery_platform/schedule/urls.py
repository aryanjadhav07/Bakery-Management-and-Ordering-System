from django.urls import path
from . import views

urlpatterns = [
    path('', views.schedule_view, name='schedule'),
    path('new/', views.schedule_class, name='schedule_class'),
]
