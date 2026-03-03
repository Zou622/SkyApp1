from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count
from .models import User
from .forms import LoginForm, UserRegistrationForm, UserProfileForm
from .decorators import admin_required
from activites.models import Activite
from clients.models import Client
from django.contrib.auth.decorators import login_required
from users.models import User
from activites.models import Activite
from django.db.models import Count
from activites.models import Activite, Client
from django.http import JsonResponse
from django.views.decorators.http import require_POST


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
                    elif user.user_type.lower() == 'technicien':
                        return redirect('clients:mes_activites')
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

    return render(request, 'utilisateurs/login.html', {'form': form})

@login_required
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

    return render(request, 'utilisateurs/register.html', {'form': form})


@login_required
def logout_view(request):
    """Déconnexion"""
    logout(request)
    messages.info(request, "👋 À bientôt !")
    return redirect('users:login')



def is_manager(user):
    return user.is_authenticated and user.user_type in ['admin', 'superviseur']


@login_required
def dashboard(request):

    user = request.user
    stats = {}

    # ==============================
    # ADMIN / SUPERVISEUR
    # ==============================
    if user.user_type in ["admin", "superviseur"]:

        stats['users'] = User.objects.count()
        stats['activites'] = Activite.objects.count()
        stats['clients'] = Client.objects.count()

    # ==============================
    # TECHNICIEN
    # ==============================
    elif user.user_type.lower() == "techniciens":

        stats['activites'] = Activite.objects.filter(
           techniciens__user=request.user
        ).distinct().count()

    # ==============================
    # COMMERCIAL
    # ==============================
    elif user.user_type == "commercial":

        stats['clients'] = Client.objects.filter(
            commercial=user
        ).count()

    context = {
        "stats": stats
    }

    return render(request, "utilisateurs/dashboard.html", context)

@admin_required
def list_utilisateurs(request):
    """Liste tous les utilisateurs (admin seulement)"""
    users = User.objects.all().order_by('-date_inscription')

    # Filtres
    user_type = request.GET.get('type', '')
    est_valide = request.GET.get('valide', '')

    if user_type:
        users = users.filter(user_type=user_type)
    if est_valide:
        users = users.filter(est_valide=(est_valide == 'true'))

    return render(request, 'utilisateurs/list_utilisateurs.html', {
        'users': users,
        'user_type_actuel': user_type,
        'types_utilisateurs': User.TYPE_USER,
    })




@login_required
@require_POST
def valider_utilisateur(request, user_id):
    user = get_object_or_404(User, id=user_id)

    user.est_valide = True
    user.save()

    return JsonResponse({
        "success": True,
        "message": f"Utilisateur {user.username} validé avec succès"
    })



@login_required
def soft_delete_utilisateur(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        user.est_actif = False  # désactive le compte
        user.save()
        return JsonResponse({"success": True, "message": "Utilisateur supprimé avec succès."})
    return JsonResponse({"success": False}, status=405)



@login_required
def modifier_profile(request):
    user = request.user
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès !")
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=user)

    return render(request, "utilisateurs/modifier_profile.html", {"form": form})


@login_required
def get_user_stats(user):
    """Statistiques selon le type d'utilisateur"""
    stats = {}

    if user.user_type == 'technicien' and user.technicien:
        activites = Activite.objects.filter(techniciens=user.technicien)
        stats['activites_total'] = activites.count()

        # ⚠️ IMPORTANT : Convertir la date en string
        aujourd_hui = timezone.now().date()
        stats['activites_aujourdhui'] = activites.filter(date_activite=aujourd_hui).count()
        # Le count() retourne un nombre, pas un objet date, donc c'est bon

        stats['en_cours'] = activites.filter(statut='en_cours').count()
        stats['planifie'] = activites.filter(statut='planifie').count()
        stats['termine'] = activites.filter(statut='termine').count()

    elif user.user_type == 'commercial' and user.commercial:
        from clients.models import Client
        stats['clients_total'] = Client.objects.filter(commercial=user.commercial).count()
        stats['clients_actifs'] = Client.objects.filter(commercial=user.commercial, statut='actif').count()

    return stats

@login_required
def profile_view(request):
    return render(request, "utilisateurs/profile.html")



@login_required
def statistiques_techniciens(request):

    # Récupérer uniquement les utilisateurs techniciens
    techniciens = User.objects.filter(role='technicien')

    # Annoter avec le nombre d'activités
    techniciens_stats = techniciens.annotate(
        total_activites=Count('activite')
    )

    context = {
        'techniciens_stats': techniciens_stats
    }

    return render(request, 'utilisateurs/dashboard.html', context)