from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
from .models import Activite, RapportActivite
from .forms import RapportActiviteForm
from techniciens.models import Technicien
from clients.models import Client

from django.contrib.auth.decorators import login_required


@login_required
def creer_rapport_activite(request, activite_id):
    """Créer un rapport pour une activité spécifique"""

    activite = get_object_or_404(Activite, id=activite_id)

    # Vérifier que le technicien est bien affecté à cette activité
    try:
        technicien = Technicien.objects.get(user=request.user)
    except Technicien.DoesNotExist:
        messages.error(request, "Vous n'êtes pas enregistré comme technicien")
        return redirect('liste_activites_technicien')

    if technicien not in activite.techniciens.all():
        messages.error(request, "Vous n'êtes pas affecté à cette activité")
        return redirect('liste_activites_technicien')

    # Vérifier si un rapport existe déjà
    if hasattr(activite, 'rapport'):
        messages.warning(request, "Un rapport existe déjà pour cette activité")
        return redirect('detail_rapport', rapport_id=activite.rapport.id)

    if request.method == 'POST':
        form = RapportActiviteForm(request.POST, request.FILES, technicien=technicien, activite=activite)

        if form.is_valid():
            rapport = form.save(commit=False)
            rapport.activite = activite
            rapport.technicien = technicien

            # Gérer l'action (brouillon ou soumission)
            action = request.POST.get('action')

            if action == 'soumettre':
                rapport.statut = 'soumis'
                activite.statut = 'termine'
                activite.heure_fin = rapport.heure_fin_reelle or datetime.now().time()
                messages.success(request, "✅ Rapport soumis avec succès !")
            else:
                rapport.statut = 'brouillon'
                messages.success(request, "📝 Rapport sauvegardé en brouillon")

            rapport.save()
            activite.save()

            return redirect('detail_rapport', rapport_id=rapport.id)
        else:
            messages.error(request, "❌ Erreur dans le formulaire. Veuillez vérifier les champs.")
    else:
        form = RapportActiviteForm(technicien=technicien, activite=activite)

    return render(request, 'activites/creer_rapport.html', {
        'form': form,
        'activite': activite,
        'technicien': technicien
    })


from django.shortcuts import render


#La liste des activté par technicien
@login_required
def liste_activites_technicien(request, technicien_id=None):
    """
    Version avec ID passé dans l'URL
    """

    if not technicien_id:
        # Si pas d'ID, prendre le premier technicien
        technicien = Technicien.objects.first()
    else:
        try:
            technicien = Technicien.objects.get(id=technicien_id)
        except Technicien.DoesNotExist:
            return render(request, 'erreur.html', {
                'message': f"Technicien avec ID {technicien_id} non trouvé."
            })

    if not technicien:
        return render(request, 'erreur.html', {
            'message': "Aucun technicien dans la base de données."
        })

    activites = Activite.objects.filter(techniciens=technicien)

    return render(request, 'rapportActivites/list_activites_par_technicien.html', {
        'activites': activites,
        'technicien': technicien,
    })

from django.utils import timezone



#La vue pour demarrer une activité
@login_required
def demarrer_activite(request, activite_id):
    """Permet au technicien de démarrer une activité"""

    activite = get_object_or_404(Activite, id=activite_id)

    try:
        technicien = Technicien.objects.get(user=request.user)
    except Technicien.DoesNotExist:
        messages.error(request, "Vous n'êtes pas enregistré comme technicien")
        return redirect('liste_activites_technicien')

    if technicien not in activite.techniciens.all():
        messages.error(request, "Vous n'êtes pas affecté à cette activité")
        return redirect('liste_activites_technicien')

    if activite.statut != 'planifie':
        messages.warning(request, "Cette activité a déjà démarré ou est terminée")
        return redirect('liste_activites_technicien')

    activite.statut = 'en_cours'
    activite.heure_debut = timezone.now().time()
    activite.save()

    messages.success(request,
                     f"✅ Activité démarrée : {activite.get_type_activite_display()} chez {activite.client.nom_client}")
    return redirect('liste_activites_technicien')