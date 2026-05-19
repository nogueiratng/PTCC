from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    nome = models.CharField("Nome Completo", max_length=255)
    cpf = models.CharField("CPF", max_length=14, unique=True)
    data_cadastro = models.DateTimeField("Data de Cadastro", auto_now_add=True)
    
    is_responsavel = models.BooleanField("É Responsável", default=True)
    is_professor = models.BooleanField("É Professor", default=False)
    area_atuacao = models.CharField("Área de Atuação", max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.nome or self.username

class Crianca(models.Model):
    nome = models.CharField("Nome", max_length=255)
    idade = models.IntegerField("Idade")
    data_nascimento = models.DateField("Data de Nascimento")
    responsavel = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        limit_choices_to={'is_responsavel': True}, 
        related_name="criancas", 
        verbose_name="Responsável"
    )

    class Meta:
        verbose_name = "Criança"
        verbose_name_plural = "Crianças"

    def __str__(self):
        return self.nome

class Atividade(models.Model):
    TIPO_CHOICES = (
        ('L', 'Letras'),
        ('N', 'Números'),
        ('C', 'Cores')
    )
    tipo = models.CharField("Tipo", max_length=1, choices=TIPO_CHOICES)
    descricao = models.CharField("Descrição", max_length=255)
    nivel = models.IntegerField("Nível")
    professor = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        limit_choices_to={'is_professor': True}, 
        related_name="atividades_validadas", 
        verbose_name="Professor Validador"
    )

    class Meta:
        verbose_name = "Atividade"
        verbose_name_plural = "Atividades"

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.descricao} (Nível {self.nivel})"

class Desempenho(models.Model):
    crianca = models.ForeignKey(Crianca, on_delete=models.CASCADE, related_name="desempenhos", verbose_name="Criança")
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE, related_name="desempenhos", verbose_name="Atividade")
    pontuacao = models.IntegerField("Pontuação")
    acertos = models.IntegerField("Acertos")
    erros = models.IntegerField("Erros")
    data_realizacao = models.DateTimeField("Data de Realização", auto_now_add=True)

    class Meta:
        verbose_name = "Desempenho"
        verbose_name_plural = "Desempenhos"

    def __str__(self):
        return f"{self.crianca.nome} - {self.atividade}"
