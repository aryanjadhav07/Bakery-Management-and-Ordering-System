from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('baker-dashboard/', views.baker_dashboard, name='baker_dashboard'),
    path('profile/', views.profile, name='profile'),
    path('select-baker/', views.select_baker, name='select_baker'),
]