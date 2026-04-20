from django.urls import path
from . import views

urlpatterns = [
    # Customer
    path('', views.course_list, name='courses'),
    path('<int:pk>/', views.course_detail, name='course_detail'),
    path('<int:pk>/enroll/', views.enroll, name='enroll'),
    path('<int:pk>/payment/', views.course_payment, name='course_payment'),
    path('enrolled/', views.enrolled_courses, name='enrolled_courses'),

    # Baker
    path('manage/', views.manage_courses, name='manage_courses'),
    path('add/', views.add_course, name='add_course'),
    path('manage/payments/', views.manage_course_payments, name='manage_course_payments'),
]
