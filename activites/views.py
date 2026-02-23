from pyexpat import model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from collections import defaultdict

from activites.models import Activite
from commercials.models import Commercial
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from datetime import date, datetime

from techniciens.models import Technicien
from .models import Client


@csrf_exempt
def activate_client(request, client_id):
    if request.method == 'POST':
        try:
            client = Client.objects.get(id=client_id)
            # Logique d'activation
            client.is_active = True
            client.save()

            return JsonResponse({
                'success': True,
                'message': f'Client {client.nom_client} activé avec succès'
            })
        except Client.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Client non trouvé'
            }, status=404)

    return JsonResponse({
        'success': False,
        'message': 'Méthode non autorisée'
    }, status=405)



#Le module des cativités
def ajouter_activite_avec_client(request, client_id):

    client = get_object_or_404(Client, id=client_id)
    techniciens = Technicien.objects.all().order_by('nom', 'prenom')

    if request.method == "POST":

        type_activite = request.POST.get("type_activite")
        date_activite = request.POST.get("date_activite")
        lieu = request.POST.get("lieu")
        description = request.POST.get("description")
        statut = request.POST.get("statut")
        heure_debut = request.POST.get("heure_debut") or None
        heure_fin = request.POST.get("heure_fin") or None

        technicien_ids = request.POST.getlist("techniciens")

        activite = Activite.objects.create(
            client=client,
            type_activite=type_activite,
            date_activite=date_activite,
            lieu=lieu,
            description=description,
            statut=statut,
            heure_debut=heure_debut,
            heure_fin=heure_fin,
        )

        # IMPORTANT pour ManyToMany
        activite.techniciens.set(technicien_ids)

        return redirect('detail_client', client_id=client_id)

    context = {
        "client": client,
        "techniciens": techniciens,
        "types_activite": Activite.TYPE_ACTIVITE_CHOICES,
        "statuts": Activite.STATUT_CHOICES,
        "aujourdhui": date.today().isoformat(),
    }

    return render(request, "clients/ajouter_activite_avec_client.html", context)


# clients/views.py

def ajouter_activite(request):
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        technicien_ids = request.POST.getlist('techniciens')
        type_activite = request.POST.get('type_activite')
        date_activite = request.POST.get('date_activite')
        heure_debut = request.POST.get('heure_debut')
        heure_fin = request.POST.get('heure_fin')
        description = request.POST.get('description', '').strip()
        lieu = request.POST.get('lieu', '').strip()
        statut = request.POST.get('statut', 'planifie')

        try:
            client = Client.objects.get(id=client_id)

            # 1️Créer l'activité SANS technicien
            activite = Activite.objects.create(
                client=client,
                type_activite=type_activite,
                date_activite=date_activite,
                heure_debut=heure_debut or None,
                heure_fin=heure_fin or None,
                description=description or None,
                lieu=lieu or None,
                statut=statut,
            )

            # Ajouter les techniciens après
            if technicien_ids:
                techniciens = Technicien.objects.filter(id__in=technicien_ids)
                activite.techniciens.set(techniciens)

            messages.success(
                request,
                f'Activité "{activite.get_type_activite_display()}" planifiée pour {client.nom_client}!'
            )

            return redirect('detail_client', client_id)

        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')

    clients = Client.objects.all().order_by('nom_client')
    techniciens = Technicien.objects.all().order_by('nom', 'prenom')

    return render(request, 'clients/ajouter_activite.html',{
        'clients': clients,
        'techniciens': techniciens,
        'types_activite': Activite.TYPE_ACTIVITE_CHOICES,
        'statuts': Activite.STATUT_CHOICES,
        'aujourdhui': date.today().isoformat(),
    })

def list_activite(request):
    """Liste toutes les activités"""
    search_query = request.GET.get('search', '')
    statut_filter = request.GET.get('statut', '')
    type_filter = request.GET.get('type', '')
    date_filter = request.GET.get('date', '')

    activites_list = Activite.objects.all()

    # Filtre de recherche
    if search_query:
        activites_list = activites_list.filter(
            Q(client__nom_client__icontains=search_query) |
            Q(technicien__nom__icontains=search_query) |
            Q(technicien__prenom__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(lieu__icontains=search_query) |
            Q(notes__icontains=search_query)
        )

    # Filtre par statut
    if statut_filter:
        activites_list = activites_list.filter(statut=statut_filter)

    # Filtre par type d'activité
    if type_filter:
        activites_list = activites_list.filter(type_activite=type_filter)

    # Filtre par date
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            activites_list = activites_list.filter(date_activite=filter_date)
        except ValueError:
            pass

    # Tri
    activites_list = activites_list.order_by('-date_activite', 'heure_debut')

    # Pagination
    paginator = Paginator(activites_list, 5)
    page_number = request.GET.get('page')
    activites = paginator.get_page(page_number)

    # Statistiques
    aujourd_hui = date.today()
    stats = {
        'total': Activite.objects.count(),
        'aujourdhui': Activite.objects.filter(date_activite=aujourd_hui).count(),
        'planifie': Activite.objects.filter(statut='planifie').count(),
        'en_cours': Activite.objects.filter(statut='en_cours').count(),
        'termine': Activite.objects.filter(statut='termine').count(),
    }

    context = {
        'activites': activites,
        'search_query': search_query,
        'statut_filter': statut_filter,
        'type_filter': type_filter,
        'date_filter': date_filter,
        'stats': stats,
        'statuts': Activite.STATUT_CHOICES,
        'types_activite': Activite.TYPE_ACTIVITE_CHOICES,
    }
    return render(request, 'clients/list_activite.html', context)


def calendrier_activites(request):
    """Vue calendrier des activités"""
    mois = request.GET.get('mois', date.today().month)
    annee = request.GET.get('annee', date.today().year)

    try:
        mois = int(mois)
        annee = int(annee)
    except ValueError:
        mois = date.today().month
        annee = date.today().year

    # Récupérer les activités du mois
    activites_mois = Activite.objects.filter(
        date_activite__year=annee,
        date_activite__month=mois
    ).order_by('date_activite')

    mois_noms_dict = {
        1: 'Janvier', 2: 'Février', 3: 'Mars', 4: 'Avril', 5: 'Mai', 6: 'Juin',
        7: 'Juillet', 8: 'Août', 9: 'Septembre', 10: 'Octobre', 11: 'Novembre', 12: 'Décembre'
    }

    context = {
        'activites': activites_mois,
        'mois': mois,
        'annee': annee,
        'mois_noms_dict': mois_noms_dict,
        'mois_range': range(1, 13),
    }

    return render(request, 'clients/calendrier_activites.html', context)


def activites_aujourdhui(request):
    """Liste des activités du jour"""
    aujourdhui = date.today()
    activites = Activite.objects.filter(date_activite=aujourdhui).order_by('heure_debut')

    context = {
        'activites': activites,
        'date': aujourdhui,
    }
    return render(request, 'clients/activites_aujourdhui.html', context)


def detail_activite(request, pk):
    """Détails d'une activité"""
    activite = get_object_or_404(Activite, pk=pk)
    context = {'activite': activite}
    return render(request, 'clients/detail_activite.html', context)


def modifier_activite(request, pk):
    """Modifier une activité"""
    activite = get_object_or_404(
        Activite.objects.prefetch_related('techniciens'),
        pk=pk
    )

    if request.method == 'POST':

        client_id = request.POST.get('client_id')
        type_activite = request.POST.get('type_activite')
        date_activite = request.POST.get('date_activite')
        heure_debut = request.POST.get('heure_debut')
        heure_fin = request.POST.get('heure_fin')
        description = request.POST.get('description', '').strip()
        lieu = request.POST.get('lieu', '').strip()
        statut = request.POST.get('statut')

        # IMPORTANT pour ManyToMany
        techniciens_ids = request.POST.getlist('techniciens')

        # Validation
        if not client_id or not type_activite or not date_activite:
            messages.error(request, 'Tous les champs obligatoires doivent être remplis')
            return redirect('modifier_activite', pk=activite.pk)

        try:
            activite.client = Client.objects.get(id=client_id)
            activite.type_activite = type_activite
            activite.date_activite = date_activite
            activite.heure_debut = heure_debut or None
            activite.heure_fin = heure_fin or None
            activite.description = description or None
            activite.lieu = lieu or None
            activite.statut = statut

            activite.save()

            # 🔥 Mise à jour ManyToMany
            activite.techniciens.set(techniciens_ids)

            messages.success(request, 'Activité modifiée avec succès!')
            return redirect('detail_activite', pk=activite.pk)

        except Exception as e:
            messages.error(request, f'Erreur: {str(e)}')

    # GET
    clients = Client.objects.all().order_by('nom_client')
    techniciens = Technicien.objects.all().order_by('nom', 'prenom')

    context = {
        'activite': activite,
        'clients': clients,
        'techniciens': techniciens,
        'types_activite': Activite.TYPE_ACTIVITE_CHOICES,
        'statuts': Activite.STATUT_CHOICES,
    }

    return render(request, 'clients/modifier_activite.html', context)

def supprimer_activite(request, pk):
    """Supprimer une activité"""
    activite = get_object_or_404(Activite, pk=pk)

    if request.method == 'POST':
        client_nom = activite.client.nom_client
        activite.delete()
        messages.success(request, f'Activité pour {client_nom} supprimée avec succès!')
        return redirect('list_activite')

    context = {'activite': activite}
    return render(request, 'activites/supprimer_activite.html', context)

#la liste des activités par client

def liste_activites_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    activites = Activite.objects.filter(client=client).order_by('-date_activite')

    context = {
        'client': client,
        'activites': activites,
    }

    return render(request, 'clients/liste_activites_client.html', context)


def activites_par_technicien(request):
    date = timezone.now().date()
    activites = Activite.objects.filter(date_activite=date).prefetch_related('techniciens', 'client')

    techniciens_dict = defaultdict(list)

    for activite in activites:
        for tech in activite.techniciens.all():
            techniciens_dict[tech].append(activite)

    context = {
        'date': date,
        'techniciens_dict': dict(techniciens_dict)
    }

    return render(request, "activites_par_technicien.html", context)