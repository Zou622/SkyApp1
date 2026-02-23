from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Technicien


# ========== VUES POUR LES TECHNICIENS ==========

def list_technicien(request):
    """Liste des techniciens avec recherche"""
    search_query = request.GET.get('search', '').strip()
    statut_filter = request.GET.get('statut', '')

    # Filtrer les techniciens
    techniciens_list = Technicien.objects.all()

    if statut_filter:
        techniciens_list = techniciens_list.filter(statut=statut_filter)

    if search_query:
        techniciens_list = techniciens_list.filter(
            Q(nom__icontains=search_query) |
            Q(prenom__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(telephone__icontains=search_query) |
            Q(quartier__icontains=search_query) |
            Q(specialite__icontains=search_query)
        )

    techniciens_list = techniciens_list.order_by('nom', 'prenom')

    # Pagination
    page = request.GET.get('page', 1)
    paginate_by = 10

    paginator = Paginator(techniciens_list, paginate_by)

    try:
        techniciens = paginator.page(page)
    except PageNotAnInteger:
        techniciens = paginator.page(1)
    except EmptyPage:
        techniciens = paginator.page(paginator.num_pages)

    # Statistiques
    total_techniciens = Technicien.objects.count()
    actif_count = Technicien.objects.filter(statut='actif').count()
    inactif_count = Technicien.objects.filter(statut='inactif').count()
    conge_count = Technicien.objects.filter(statut='congé').count()
    mission_count = Technicien.objects.filter(statut='mission').count()

    context = {
        'techniciens': techniciens,
        'search_query': search_query,
        'statut_filter': statut_filter,
        'total_techniciens': total_techniciens,
        'actif_count': actif_count,
        'inactif_count': inactif_count,
        'conge_count': conge_count,
        'mission_count': mission_count,
    }

    return render(request, 'techniciens/list_technicien.html', context)


def ajouter_technicien(request):
    """Afficher le formulaire d'ajout de technicien"""
    return render(request, 'techniciens/ajouter_technicien.html')


def enregistrer_technicien(request):
    """Enregistrer un nouveau technicien"""
    if request.method == 'POST':
        # Récupérer les données
        nom = request.POST.get('nom', '').strip()
        prenom = request.POST.get('prenom', '').strip()
        email = request.POST.get('email', '').strip()
        telephone = request.POST.get('telephone', '').strip()
        quartier = request.POST.get('quartier', '').strip()
        adresse = request.POST.get('adresse', '').strip()
        specialite = request.POST.get('specialite', '').strip()
        statut = request.POST.get('statut', 'actif').strip()
        date_embauche = request.POST.get('date_embauche', '').strip()
        photo = request.FILES.get('photo')

        # Validation
        if not nom or not prenom or not email:
            messages.error(request, 'Le nom, prénom et email sont obligatoires')
            return render(request, 'techniciens/ajouter_technicien.html')

        # Vérifier si l'email existe déjà
        if Technicien.objects.filter(email=email).exists():
            messages.error(request, f'Un technicien avec l\'email "{email}" existe déjà')
            return render(request, 'techniciens/ajouter_technicien.html')

        # Créer et sauvegarder le technicien
        technicien = Technicien(
            nom=nom,
            prenom=prenom,
            email=email,
            telephone=telephone,
            quartier=quartier,
            adresse=adresse,
            specialite=specialite,
            statut=statut,
            date_embauche=date_embauche,
            photo=photo
        )
        technicien.save()

        messages.success(request, f'✅ Technicien "{nom} {prenom}" ajouté avec succès!')
        return redirect('list_technicien')

    return redirect('ajouter_technicien')


def detail_technicien(request, technicien_id):
    """Afficher les détails d'un technicien"""
    technicien = get_object_or_404(Technicien, id=technicien_id)
    return render(request, 'techniciens/detail_technicien.html', {'technicien': technicien})


def modifier_technicien(request, technicien_id):
    """Modifier un technicien existant"""
    technicien = get_object_or_404(Technicien, id=technicien_id)

    if request.method == 'POST':
        # Mettre à jour les données
        technicien.nom = request.POST.get('nom', technicien.nom)
        technicien.prenom = request.POST.get('prenom', technicien.prenom)
        technicien.email = request.POST.get('email', technicien.email)
        technicien.telephone = request.POST.get('telephone', technicien.telephone)
        technicien.quartier = request.POST.get('quartier', technicien.quartier)
        technicien.adresse = request.POST.get('adresse', technicien.adresse)
        technicien.specialite = request.POST.get('specialite', technicien.specialite)
        technicien.statut = request.POST.get('statut', technicien.statut)
        technicien.date_embauche = request.POST.get('date_embauche', technicien.date_embauche)

        if 'photo' in request.FILES:
            technicien.photo = request.FILES['photo']

        technicien.save()
        messages.success(request, f'✅ Technicien "{technicien.nom} {technicien.prenom}" modifié avec succès!')
        return redirect('list_technicien')

    return render(request, 'techniciens/modifier_technicien.html', {'technicien': technicien})


def supprimer_technicien(request, technicien_id):
    """Supprimer un technicien"""
    technicien = get_object_or_404(Technicien, id=technicien_id)

    if request.method == 'POST':
        nom_complet = f"{technicien.nom} {technicien.prenom}"
        technicien.delete()
        messages.success(request, f'❌ Technicien "{nom_complet}" supprimé avec succès!')
        return redirect('list_technicien')

    return render(request, 'techniciens/supprimer_technicien.html', {'technicien': technicien})