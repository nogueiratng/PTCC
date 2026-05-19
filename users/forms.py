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
    # O Formulário de Cadastro fica bem enxuto, pois herda tudo do UserCreationForm
    class Meta(UserCreationForm.Meta):
        model = Usuario 
        fields = ('username', 'nome', 'cpf', 'email', 'is_professor')
