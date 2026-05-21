from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.http import JsonResponse
import json
from .forms import ProfileForm, RegisterForm, CriancaForm, AtividadeForm, PerguntaForm
from .models import Crianca, Atividade, Pergunta, Desempenho

@login_required
def dashboard(request):
    """View para o dashboard do usuário"""
    if request.user.is_professor:
        atividades = request.user.atividades_validadas.all()
        return render(request, 'dashboard_professor.html', {'atividades': atividades})
    
    if request.user.is_responsavel:
        criancas = request.user.criancas.all()
    else:
        criancas = None
    return render(request, 'dashboard.html', {'criancas': criancas})

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

def register_view(request):
    """View para criar uma nova conta de usuário"""
    if request.user.is_authenticated:
        return redirect('users:dashboard')
        
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Logar o usuário automaticamente após o cadastro (opcional)
            login(request, user)
            messages.success(request, 'Conta criada com sucesso! Bem-vindo(a)!')
            return redirect('users:dashboard')
    else:
        form = RegisterForm()
        
    return render(request, 'register.html', {'form': form})

@login_required
def adicionar_crianca_view(request):
    """View para cadastrar um novo filho"""
    # Se não for responsável, redireciona
    if not request.user.is_responsavel:
        messages.error(request, 'Apenas responsáveis podem cadastrar crianças.')
        return redirect('users:dashboard')
        
    if request.method == 'POST':
        form = CriancaForm(request.POST)
        if form.is_valid():
            crianca = form.save(commit=False)
            crianca.responsavel = request.user
            crianca.save()
            messages.success(request, f'Criança {crianca.nome} cadastrada com sucesso!')
            return redirect('users:dashboard')
    else:
        form = CriancaForm()
        
    return render(request, 'adicionar_crianca.html', {'form': form})

@login_required
def criar_atividade_view(request):
    """View para o professor cadastrar uma nova atividade"""
    if not request.user.is_professor:
        messages.error(request, 'Apenas professores podem cadastrar atividades.')
        return redirect('users:dashboard')
        
    if request.method == 'POST':
        form = AtividadeForm(request.POST)
        if form.is_valid():
            atividade = form.save(commit=False)
            atividade.professor = request.user
            atividade.save()
            messages.success(request, 'Atividade cadastrada com sucesso!')
            return redirect('users:dashboard')
    else:
        form = AtividadeForm()
        
    return render(request, 'criar_atividade.html', {'form': form})

@login_required
def adicionar_pergunta_view(request, atividade_id):
    """View para o professor adicionar uma pergunta a uma atividade"""
    if not request.user.is_professor:
        return redirect('users:dashboard')
        
    atividade = get_object_or_404(Atividade, id=atividade_id, professor=request.user)
    
    if request.method == 'POST':
        form = PerguntaForm(request.POST)
        if form.is_valid():
            pergunta = form.save(commit=False)
            pergunta.atividade = atividade
            pergunta.save()
            messages.success(request, 'Pergunta adicionada com sucesso!')
            return redirect('users:dashboard') # No futuro podemos redirecionar de volta pra adicionar mais
    else:
        form = PerguntaForm()
        
    return render(request, 'adicionar_pergunta.html', {'form': form, 'atividade': atividade})

@login_required
def jogar_atividade_view(request, atividade_id):
    """View que carrega a tela do jogo e manda os dados das perguntas em JSON"""
    if not request.user.is_responsavel:
        messages.error(request, 'Apenas crianças através dos responsáveis podem jogar.')
        return redirect('users:dashboard')
        
    atividade = get_object_or_404(Atividade, id=atividade_id)
    perguntas = atividade.perguntas.all()
    
    # Prepara os dados das perguntas para o Javascript ler
    perguntas_data = []
    for p in perguntas:
        perguntas_data.append({
            'enunciado': p.enunciado,
            'opcoes': {
                'A': p.opcao_a,
                'B': p.opcao_b,
                'C': p.opcao_c
            },
            'correta': p.resposta_correta
        })
        
    # Precisa saber qual criança está jogando.
    # Por enquanto, como o pai escolhe, vamos supor que ele passa o ID na URL ou apenas escolhe o primeiro filho para teste
    crianca = request.user.criancas.first()
    if not crianca:
        messages.error(request, 'Você precisa cadastrar uma criança primeiro.')
        return redirect('users:dashboard')
        
    context = {
        'atividade': atividade,
        'perguntas_json': perguntas_data,
        'crianca': crianca
    }
    return render(request, 'jogo.html', context)

@login_required
def salvar_desempenho_api(request):
    """API invisível chamada pelo JS para salvar os pontos da criança ao final do jogo"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            crianca_id = data.get('crianca_id')
            atividade_id = data.get('atividade_id')
            acertos = int(data.get('acertos', 0))
            erros = int(data.get('erros', 0))
            pontuacao = int(data.get('pontuacao', 0))
            
            crianca = get_object_or_404(Crianca, id=crianca_id, responsavel=request.user)
            atividade = get_object_or_404(Atividade, id=atividade_id)
            
            Desempenho.objects.create(
                crianca=crianca,
                atividade=atividade,
                acertos=acertos,
                erros=erros,
                pontuacao=pontuacao
            )
            return JsonResponse({'status': 'success', 'message': 'Desempenho salvo!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)

@login_required
def iniciar_jogo_view(request, tipo):
    """Roteador inteligente: encontra a próxima atividade não-concluída pela criança"""
    if not request.user.is_responsavel:
        messages.error(request, 'Apenas responsáveis podem iniciar jogos.')
        return redirect('users:dashboard')

    # Pega a primeira criança do responsável (futuramente pode ter seleção)
    crianca = request.user.criancas.first()
    if not crianca:
        messages.error(request, 'Cadastre uma criança primeiro para poder jogar!')
        return redirect('users:dashboard')

    # IDs das atividades que essa criança já jogou
    atividades_ja_feitas = Desempenho.objects.filter(
        crianca=crianca
    ).values_list('atividade_id', flat=True)

    # Busca atividades do tipo pedido, com perguntas cadastradas, que ainda não foram feitas
    proxima_atividade = Atividade.objects.filter(
        tipo=tipo,
        perguntas__isnull=False
    ).exclude(
        id__in=atividades_ja_feitas
    ).distinct().first()

    if proxima_atividade:
        # Criança tem uma atividade nova! Redireciona para o jogo.
        return redirect('users:jogar_atividade', atividade_id=proxima_atividade.id)
    else:
        # Verifica se existem atividades desse tipo (mas a criança já fez todas)
        total_atividades = Atividade.objects.filter(tipo=tipo, perguntas__isnull=False).distinct().count()
        tipo_display = {'L': 'Letras', 'N': 'Números', 'C': 'Cores'}.get(tipo, tipo)

        if total_atividades > 0:
            messages.success(request, f'🏆 Parabéns! Você já completou todos os desafios de {tipo_display}! Aguarde novos desafios em breve.')
        else:
            messages.info(request, f'Ainda não há jogos de {tipo_display} disponíveis. Fique de olho!')

        return redirect('users:dashboard')