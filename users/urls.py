from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('cadastro/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('perfil/', views.profile_view, name='perfil'),
    path('configuracoes/', views.settings_view, name='configuracoes'),
    path('logout/', views.logout_view, name='logout'),
    path('adicionar-filho/', views.adicionar_crianca_view, name='adicionar_crianca'),
    path('criar-atividade/', views.criar_atividade_view, name='criar_atividade'),
    path('atividade/<int:atividade_id>/adicionar-pergunta/', views.adicionar_pergunta_view, name='adicionar_pergunta'),
    path('jogar/<int:atividade_id>/', views.jogar_atividade_view, name='jogar_atividade'),
    path('api/salvar-desempenho/', views.salvar_desempenho_api, name='salvar_desempenho'),
    path('iniciar/<str:tipo>/', views.iniciar_jogo_view, name='iniciar_jogo'),
    path('desempenho/', views.desempenho_view, name='desempenho'),
]