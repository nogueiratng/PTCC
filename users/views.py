from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages

@login_required
def dashboard(request):
    """View para o dashboard do usuário"""
    return render(request, 'dashboard.html')

def login_view(request):
    """View para login do usuário"""
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
