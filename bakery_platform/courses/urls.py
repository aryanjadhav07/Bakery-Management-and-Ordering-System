from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='courses'),
    path('<int:pk>/', views.course_detail, name='course_detail'),
    path('<int:pk>/enroll/', views.enroll, name='enroll'),
    path('enrolled/', views.enrolled_courses, name='enrolled_courses'),
    path('manage/', views.manage_courses, name='manage_courses'),
    path('add/', views.add_course, name='add_course'),
]
