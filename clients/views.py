from pyexpat import model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from collections import defaultdict
from django.contrib.auth.decorators import login_required, user_passes_test
from activites.models import Activite
from commercials.models import Commercial
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from datetime import date, datetime

from techniciens.models import Technicien
#from rapportActivites.models import RapportActivite
from .models import Client
from users.models import User
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from activites.models import Activite
from .decorators import technicien_required, role_required, admin_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, user_passes_test





def is_manager(user):
    return user.is_authenticated and user.user_type in ['admin', 'superviseur']

# fonction pour afficher le formulaire de Acceuil.
@login_required
def acceuil(request):
    return  render(request,'clients/Acceuil.html')



@login_required
@user_passes_test(is_manager)
def afficher_formulaire_ajout(request):
    # Récupérer tous les commerciaux
    commerciaux = Commercial.objects.all()
    client = None  # Aucun client existant lors de l'ajout

    return render(request, 'clients/Add_client.html', {
        'commerciaux': commerciaux,
        'client': client
    })

@login_required
@user_passes_test(is_manager)
def enregistrer_client(request):
    if request.method == 'POST':
        nom_client = request.POST.get('nom_client', '').strip()
        adresse = request.POST.get('adresse', '').strip()
        quartier = request.POST.get('quartier', '').strip()
        telephone = request.POST.get('telephone', '').strip()
        email = request.POST.get('email', '').strip()
        vlan = request.POST.get('vlan', '').strip()
        adresse_ip = request.POST.get('adresse_ip', '').strip()
        statut = request.POST.get('statut', 'non_actif').strip()
        type_contrat = request.POST.get('type_contrat', '').strip()
        capacite = request.POST.get('capacite', '').strip()
        download = request.POST.get('download', '').strip()
        upload = request.POST.get('upload', '').strip()
        contrat_pdf = request.FILES.get('contrat_pdf')

        # ✅ CORRECTION ICI
        commercial_id = request.POST.get('commercial_id')

        commercial = None
        if commercial_id:
            try:
                commercial = Commercial.objects.get(id=commercial_id)
            except Commercial.DoesNotExist:
                commercial = None

        client = Client.objects.create(
            nom_client=nom_client,
            adresse=adresse,
            quartier=quartier,
            telephone=telephone,
            email=email,
            vlan=vlan,
            adresse_ip=adresse_ip,
            statut=statut,
            type_contrat=type_contrat,
            capacite=capacite or None,
            download=download or None,
            upload=upload or None,
            contrat_pdf=contrat_pdf,
            commercial=commercial
        )

        messages.success(request, f'✅ Client "{nom_client}" ajouté avec succès!')
        return redirect('clients:list_client')

    return redirect('clients:afficher_formulaire')







@login_required
@user_passes_test(is_manager)
def list_client(request):
    """
    Vue pour afficher la liste des clients avec statistiques
    """
    # Votre logique de filtrage existante
    #clients = Client.objects.all()
    clients = Client.objects.select_related('commercial').order_by('-id')

    # Filtrage par statut
    statut_filter = request.GET.get('statut')
    if statut_filter:
        clients = clients.filter(statut=statut_filter)

    # Recherche par texte
    search_query = request.GET.get('search', '')
    if search_query:
        clients = clients.filter(
            Q(nom_client__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(telephone__icontains=search_query)
        )

    # Calcul des statistiques (sur tous les clients)
    total_clients = Client.objects.all().count()
    actif_count = Client.objects.filter(statut='actif').count()
    suspendu_count = Client.objects.filter(statut='suspendu').count()
    resilie_count = Client.objects.filter(statut='resilie').count()
    non_actif_count = Client.objects.filter(statut='non_actif').count()

    # Calcul des pourcentages
    if total_clients > 0:
        actif_pourcentage = round((actif_count / total_clients) * 100, 1)
        suspendu_pourcentage = round((suspendu_count / total_clients) * 100, 1)
        resilie_pourcentage = round((resilie_count / total_clients) * 100, 1)
        non_actif_pourcentage = round((non_actif_count / total_clients) * 100, 1)
    else:
        actif_pourcentage = suspendu_pourcentage = resilie_pourcentage = non_actif_pourcentage = 0

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(clients, 5)

    try:
        clients_paginated = paginator.page(page)
    except PageNotAnInteger:
        clients_paginated = paginator.page(1)
    except EmptyPage:
        clients_paginated = paginator.page(paginator.num_pages)

    # Déterminer la plage de pages à afficher
    page_num = clients_paginated.number
    if paginator.num_pages <= 7:
        page_range = range(1, paginator.num_pages + 1)
    else:
        if page_num <= 4:
            page_range = range(1, 8)
        elif page_num >= paginator.num_pages - 3:
            page_range = range(paginator.num_pages - 6, paginator.num_pages + 1)
        else:
            page_range = range(page_num - 3, page_num + 4)

    context = {
        'clients': clients_paginated,
        'total_clients': total_clients,
        'actif_count': actif_count,
        'suspendu_count': suspendu_count,
        'resilie_count': resilie_count,
        'non_actif_count': non_actif_count,
        'actif_pourcentage': actif_pourcentage,
        'suspendu_pourcentage': suspendu_pourcentage,
        'resilie_pourcentage': resilie_pourcentage,
        'non_actif_pourcentage': non_actif_pourcentage,
        'search_query': search_query,
        'statut_filter': statut_filter,
        'page_range': page_range,
    }
    return render(request, 'clients/list_client.html', context)

# Pour que les statistiques s'affichent correctement, modifiez aussi le template HTML :
# Remplacez {{ stats.actif|default:0 }} par {{ stats.actif|default:"0" }}
# Remplacez {{ stats.suspendu|default:0 }} par {{ stats.suspendu|default:"0" }}
# Remplacez {{ stats.resilie|default:0 }} par {{ stats.resilie|default:"0" }}


@login_required
@user_passes_test(is_manager)
#fonction pour afficher le formulaire detail.
def detail_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    return render(request, 'clients/detail_client.html', {'client': client})



@login_required
@user_passes_test(is_manager)
#Fonction pour la modification d'un client
def modifier_client(request, client_id):
    """Modifier un client existant"""

    client = get_object_or_404(Client, id=client_id)

    if request.method == 'POST':
        # Récupération des données du formulaire
        client.nom_client = request.POST.get('nom_client', client.nom_client)
        client.adresse = request.POST.get('adresse', client.adresse)
        client.quartier = request.POST.get('quartier', client.quartier)
        client.telephone = request.POST.get('telephone', client.telephone)
        client.email = request.POST.get('email', client.email)
        client.vlan = request.POST.get('vlan', client.vlan)
        client.statut = request.POST.get('statut', client.statut)
        client.adresse_ip = request.POST.get('adresse_ip', client.adresse_ip)
        client.type_contrat = request.POST.get('type_contrat', client.type_contrat)
        client.capacite = request.POST.get('capacite', client.capacite)
        client.download = request.POST.get('download', client.download)
        client.upload = request.POST.get('upload', client.upload)

        # Gestion du commercial
        commercial_id = request.POST.get('commercial_id')

        if commercial_id and commercial_id.isdigit():
            try:
                client.commercial = Commercial.objects.get(id=commercial_id)
            except Commercial.DoesNotExist:
                client.commercial = None
                messages.warning(request, '⚠️ Le commercial sélectionné n\'existe pas')
        else:
            client.commercial = None  # si aucun commercial sélectionné

        # Gestion du fichier PDF
        if 'contrat_pdf' in request.FILES:
            # Supprimer l'ancien fichier si nécessaire
            if client.contrat_pdf:
                client.contrat_pdf.delete(save=False)
            client.contrat_pdf = request.FILES['contrat_pdf']

        # Sauvegarde du client
        client.save()

        messages.success(request, f'✅ Client "{client.nom_client}" modifié avec succès!')
        return redirect('clients:list_client')

    # Pour l'affichage du formulaire (GET)
    commerciaux = Commercial.objects.all().order_by('nom', 'prenom')

    # Vous pouvez aussi filtrer les commerciaux actifs si vous avez ce champ
    # commerciaux = Commercial.objects.filter(actif=True).order_by('nom', 'prenom')

    return render(
        request,
        'clients/modifier_client.html',
        {
            'client': client,
            'commerciaux': commerciaux
        }
    )

@login_required
@user_passes_test(is_manager)
#Fonction pour la suppression d'un client
def supprimer_client(request, client_id):
    """Supprimer un client"""
    client = get_object_or_404(Client, id=client_id)

    if request.method == 'POST':
        nom_client = client.nom_client
        client.delete()
        messages.success(request, f'❌ Client "{nom_client}" supprimé avec succès!')
        return redirect('list_client')

    return render(request, 'clients/supprimer_client.html', {'client': client})


@login_required
@user_passes_test(is_manager)
#Fonction pour afficher le pdf
def voir_pdf(request, client_id):
        """Afficher le PDF d'un client"""
        client = get_object_or_404(Client, id=client_id)

        if client.contrat_pdf:
            # Ouvrir le fichier PDF
            pdf_file = open(client.contrat_pdf.path, 'rb')

            # Retourner le PDF comme réponse
            response = FileResponse(pdf_file, content_type='application/pdf')

            # Optionnel: afficher dans le navigateur plutôt que télécharger
            response['Content-Disposition'] = f'inline; filename="{client.contrat_pdf.name}"'

            return response
        else:
            messages.error(request, "Aucun fichier PDF disponible")
            return redirect('detail_client', client_id=client_id)


@login_required
@user_passes_test(is_manager)
#//fonction pour l'activation du client'
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



@login_required
@user_passes_test(is_manager)   
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

        return redirect('clients:detail_client', client_id=client_id)

    context = {
        "client": client,
        "techniciens": techniciens,
        "types_activite": Activite.TYPE_ACTIVITE_CHOICES,
        "statuts": Activite.STATUT_CHOICES,
        "aujourdhui": date.today().isoformat(),
    }

    return render(request, "clients/ajouter_activite_avec_client.html", context)


# clients/views.py

@login_required
@user_passes_test(is_manager)   
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

            return redirect('clients:detail_client', client_id)

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

@login_required
@user_passes_test(is_manager)   
def list_activite(request):
    # 🔐 Si technicien → il ne voit que ses activités
    if request.user.user_type.lower() == "technicien":

        if not hasattr(request.user, "technicien"):
            return redirect("dashboard")

        technicien = request.user.technicien

        activites_list = Activite.objects.filter(
            techniciens=technicien
        )

    else:
        # Admin / Superviseur / Commercial
        activites_list = Activite.objects.all()


    """Liste toutes les activités"""
    search_query = request.GET.get('search', '')
    statut_filter = request.GET.get('statut', '')
    type_filter = request.GET.get('type', '')
    date_filter = request.GET.get('date', '')



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


@login_required
@user_passes_test(is_manager)
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


@login_required
@user_passes_test(is_manager)
def activites_aujourdhui(request):
    """Liste des activités du jour"""
    aujourdhui = date.today()
    activites = Activite.objects.filter(date_activite=aujourdhui).order_by('heure_debut')

    context = {
        'activites': activites,
        'date': aujourdhui,
    }
    return render(request, 'clients/activites_aujourdhui.html', context)


@login_required
@user_passes_test(is_manager)   
def detail_activite(request, id):
    """Détails d'une activité"""
    activite = get_object_or_404(Activite, pk=id)
    context = {'activite': activite}
    return render(request, 'clients/detail_activite.html', context)

@login_required
@user_passes_test(is_manager)
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
        if hasattr(request.user, 'technicien'):
            #raise PermissionDenied
            pass

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

@login_required
@user_passes_test(is_manager)
def supprimer_activite(request, pk):
    """Supprimer une activité"""
    activite = get_object_or_404(Activite, pk=pk)

    if hasattr(request.user, 'technicien'):
        raise PermissionDenied

    if request.method == 'POST':
        client_nom = activite.client.nom_client
        activite.delete()
        messages.success(request, f'Activité pour {client_nom} supprimée avec succès!')
        return redirect('list_activite')

    context = {'activite': activite}
    return render(request, 'activites/supprimer_activite.html', context)

#la liste des activités par client


@login_required
@user_passes_test(is_manager)
def liste_activites_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    activites = Activite.objects.filter(client=client).order_by('-date_activite')

    context = {
        'client': client,
        'activites': activites,
    }

    return render(request, 'clients/liste_activites_client.html', context)

@login_required
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


#La vue des mes activités pour les techniciens connectés


@login_required
def mes_activites(request):
    # Utiliser getattr pour éviter l'exception AttributeError
    technicien = getattr(request.user, 'technicien', None)
    
    if not technicien:
        return HttpResponseForbidden("Vous n'êtes pas associé à un profil technicien")
    
    activites = Activite.objects.filter(techniciens=technicien)
    return render(request, 'clients/mes_activites.html', {'activites': activites})

@login_required
def detail_activite(request, id):
    #technicien = request.user.technicien
    activite = get_object_or_404(
        Activite,
        id=id,
        #techniciens=technicien
    )

    return render(request, 'clients/detail_activite.html', {
        'activite': activite
    })
