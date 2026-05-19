from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class ProfileForm(forms.ModelForm):
    # Campos extras que não fazem parte direto do Meta (para troca de senha do usuário já logado)
    password = forms.CharField(
        label='Nova senha',
        widget=forms.PasswordInput,
        required=False,
        help_text='Deixe em branco para manter a mesma senha.'
    )
    password_confirm = forms.CharField(
        label='Confirmar nova senha',
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = Usuario
        fields = ['nome', 'email']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Seu nome completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Seu melhor e-mail'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        # Validação extra de segurança apenas se o usuário tentar alterar a senha
        if password or password_confirm:
            if password != password_confirm:
                raise forms.ValidationError('As senhas devem ser iguais.')
            if len(password) < 8:
                raise forms.ValidationError('A senha precisa ter ao menos 8 caracteres.')
        return cleaned_data


class RegisterForm(UserCreationForm):
    # Criamos as opções de seleção
    TIPO_CHOICES = (
        ('responsavel', 'Sou Responsável (Pai/Mãe)'),
        ('professor', 'Sou Professor(a)'),
    )
    
    # Criamos um campo visual de Seleção (Dropdown)
    tipo_conta = forms.ChoiceField(
        choices=TIPO_CHOICES, 
        label="Tipo de Conta",
        widget=forms.Select(attrs={'style': 'width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 5px; font-size: 1rem; box-sizing: border-box; background: white;'})
    )

    class Meta(UserCreationForm.Meta):
        model = Usuario 
        fields = ('username', 'nome', 'cpf', 'email')
        
    def save(self, commit=True):
        # Pausa o salvamento automático para ajustarmos as flags
        user = super().save(commit=False)
        tipo = self.cleaned_data.get('tipo_conta')
        
        # Define as permissões com base no que a pessoa escolheu na tela
        if tipo == 'professor':
            user.is_professor = True
            user.is_responsavel = False
        else:
            user.is_responsavel = True
            user.is_professor = False
            
        # Agora sim salva no banco de dados
        if commit:
            user.save()
        return user

from datetime import date
from .models import Crianca

class CriancaForm(forms.ModelForm):
    class Meta:
        model = Crianca
        # Só pedimos o nome e data de nascimento na tela
        fields = ['nome', 'data_nascimento']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nome da criança'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }

    def save(self, commit=True):
        # Pausa o salvamento para calcularmos a idade
        crianca = super().save(commit=False)
        
        # Calcula a idade baseada na data de nascimento
        hoje = date.today()
        nasc = self.cleaned_data.get('data_nascimento')
        idade = hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))
        
        # Preenche o campo idade que o banco exige
        crianca.idade = idade
        
        if commit:
            crianca.save()
        return crianca
