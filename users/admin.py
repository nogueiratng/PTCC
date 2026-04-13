from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Responsavel, Crianca, Atividade, Desempenho, Professor


@admin.register(Responsavel)
class ResponsavelAdmin(UserAdmin):
    list_display = ('username', 'nome', 'email', 'cpf', 'data_cadastro', 'is_staff')
    search_fields = ('username', 'nome', 'email', 'cpf')
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('nome', 'cpf')}),
    )

@admin.register(Crianca)
class CriancaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'idade', 'data_nascimento', 'responsavel')
    search_fields = ('nome', 'responsavel__nome')
    list_filter = ('idade',)

@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'descricao', 'nivel', 'professor')
    list_filter = ('tipo', 'nivel', 'professor')
    search_fields = ('descricao',)

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'area_atuacao', 'data_cadastro')
    search_fields = ('nome', 'cpf', 'area_atuacao')
    list_filter = ('area_atuacao',)

@admin.register(Desempenho)
class DesempenhoAdmin(admin.ModelAdmin):
    list_display = ('crianca', 'atividade', 'pontuacao', 'acertos', 'erros', 'data_realizacao')
    list_filter = ('atividade__tipo', 'data_realizacao')
    search_fields = ('crianca__nome', 'atividade__descricao')
