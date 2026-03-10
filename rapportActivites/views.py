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
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from activites.models import Activite


from django.shortcuts import render, get_object_or_404, redirect
from .forms import RapportActiviteForm
from activites.models import Activite


def creer_rapport(request, activite_id):

    activite = get_object_or_404(Activite, id=activite_id)

    if request.method == "POST":

        form = RapportActiviteForm(
            request.POST,
            request.FILES,
            activite=activite
        )

        if form.is_valid():
            rapport = form.save(commit=False)
            rapport.activite = activite
            rapport.save()

    else:

        form = RapportActiviteForm(activite=activite)

    return render(request, "rapportsActivites/creer_rapport.html", {
        "form": form,
        "activite": activite
    })


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