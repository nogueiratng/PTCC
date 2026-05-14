from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('perfil/', views.profile_view, name='perfil'),
    path('configuracoes/', views.settings_view, name='configuracoes'),
    path('logout/', views.logout_view, name='logout'),
]