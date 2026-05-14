from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages

from .forms import ProfileForm

@login_required
def dashboard(request):
    """View para o dashboard do usuário"""
    return render(request, 'dashboard.html')

@login_required
def profile_view(request):
    """View para edição de perfil do usuário"""
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            password_confirm = form.cleaned_data.get('password_confirm')
            if password or password_confirm:
                if password != password_confirm:
                    messages.error(request, 'As senhas não conferem.')
                else:
                    user.set_password(password)
                    update_session_auth_hash(request, user)
                    form.save(commit=False)
                    user.email = form.cleaned_data.get('email')
                    user.nome = form.cleaned_data.get('nome')
                    user.save()
                    messages.success(request, 'Dados do perfil atualizados com sucesso.')
            else:
                form.save()
                messages.success(request, 'Dados do perfil atualizados com sucesso.')
            return redirect('users:perfil')
    else:
        form = ProfileForm(instance=user)
    return render(request, 'profile.html', {'form': form})

@login_required
def settings_view(request):
    """View para acessibilidade e configurações úteis"""
    return render(request, 'settings.html')

@login_required
def logout_view(request):
    """Encerrar sessão e voltar para login"""
    logout(request)
    messages.success(request, 'Você saiu com sucesso.')
    return redirect('users:login')

def login_view(request):
    """View para login do usuário"""
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('users:dashboard')
        else:
            messages.error(request, 'Credenciais inválidas. Tente novamente.')
    return render(request, 'login.html')
