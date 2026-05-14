from django import forms
from .models import Responsavel

class ProfileForm(forms.ModelForm):
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
        model = Responsavel
        fields = ['nome', 'email']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Seu nome completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Seu melhor e-mail'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password or password_confirm:
            if password != password_confirm:
                raise forms.ValidationError('As senhas devem ser iguais.')
            if len(password) < 8:
                raise forms.ValidationError('A senha precisa ter ao menos 8 caracteres.')
        return cleaned_data
