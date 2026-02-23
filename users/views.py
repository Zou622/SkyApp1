from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import User
from .forms import LoginForm, UserRegistrationForm, UserProfileForm
from .decorators import admin_required
from activites.models import Activite


def login_view(request):
    """Vue de connexion"""
    if request.user.is_authenticated:
        return redirect('users:dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.est_actif and user.est_valide:
                    login(request, user)
                    user.derniere_connexion = timezone.now()
                    user.save()

                    messages.success(request, f"✅ Bienvenue {user.get_full_name()}!")

                    # Redirection selon le type
                    if user.user_type == 'admin':
                        return redirect('users:dashboard')
                    elif user.user_type == 'technicien':
                        return redirect('rapportActivites:liste_activites_technicien')
                    elif user.user_type == 'commercial':
                        return redirect('clients:list_client')
                    else:
                        return redirect('users:dashboard')
                else:
                    messages.error(request, "⛔ Votre compte n'est pas actif ou validé")
        else:
            messages.error(request, "❌ Nom d'utilisateur ou mot de passe incorrect")
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def register_view(request):
    """Vue d'inscription"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.est_valide = False  # À valider par un admin
            user.save()

            messages.success(
                request,
                "✅ Inscription réussie ! Votre compte sera validé par un administrateur."
            )
            return redirect('users:login')
        else:
            messages.error(request, "❌ Erreur dans le formulaire")
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def logout_view(request):
    """Déconnexion"""
    logout(request)
    messages.info(request, "👋 À bientôt !")
    return redirect('users:login')


@login_required
def dashboard(request):
    """Dashboard principal"""
    context = {
        'user': request.user,
        'stats': get_user_stats(request.user),
    }
    return render(request, 'users/dashboard.html', context)


@login_required
def profile_view(request):
    """Vue du profil"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Profil mis à jour avec succès")
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'users/profile.html', {'form': form})


@login_required
@admin_required
def liste_utilisateurs(request):
    """Liste tous les utilisateurs (admin seulement)"""
    users = User.objects.all().order_by('-date_inscription')

    # Filtres
    user_type = request.GET.get('type', '')
    est_valide = request.GET.get('valide', '')

    if user_type:
        users = users.filter(user_type=user_type)
    if est_valide:
        users = users.filter(est_valide=(est_valide == 'true'))

    return render(request, 'users/admin/liste_utilisateurs.html', {
        'users': users,
        'user_type_actuel': user_type,
        'types_utilisateurs': User.TYPE_USER,
    })


@login_required
@admin_required
def valider_utilisateur(request, user_id):
    """Valide un utilisateur (admin seulement)"""
    user = get_object_or_404(User, id=user_id)
    user.est_valide = True
    user.save()
    messages.success(request, f"✅ Utilisateur {user.username} validé avec succès")
    return redirect('users:liste_utilisateurs')


def get_user_stats(user):
    """Statistiques selon le type d'utilisateur"""
    stats = {}

    if user.user_type == 'technicien' and user.technicien:
        activites = Activite.objects.filter(techniciens=user.technicien)
        stats['activites_total'] = activites.count()
        stats['activites_aujourdhui'] = activites.filter(date_activite=timezone.now().date()).count()
        stats['en_cours'] = activites.filter(statut='en_cours').count()
        stats['planifie'] = activites.filter(statut='planifie').count()
        stats['termine'] = activites.filter(statut='termine').count()

    elif user.user_type == 'commercial' and user.commercial:
        from clients.models import Client
        stats['clients_total'] = Client.objects.filter(commercial=user.commercial).count()
        stats['clients_actifs'] = Client.objects.filter(commercial=user.commercial, statut='actif').count()

    return stats