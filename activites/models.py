from django.db import models
from datetime import date, datetime

from techniciens.models import Technicien
from clients.models import Client


class Activite(models.Model):
    TYPE_ACTIVITE_CHOICES = [
        ('dementelement', 'Démantèlement'),
        ('survey', 'Survey'),
        ('installation', 'Installation'),
        ('investigation', 'Investigation'),
        ('maintenance', 'Maintenance'),
        ('tirage', 'Tirage'),
        ('raccordement', 'Raccordement'),
        ('remplacement', 'Remplacement'),
        ('autre', 'Autre'),
    ]

    STATUT_CHOICES = [
        ('planifie', 'Planifié'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('annule', 'Annulé'),
        ('reporte', 'Reporté'),
    ]

    # Relations - Django créera automatiquement client_id
    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.CASCADE,
        verbose_name="Client",
        db_column='client_id'  # Optionnel, Django le fait déjà
    )

    #Relation de 1 à plusieurs technicien
    techniciens = models.ManyToManyField(Technicien,blank=True,related_name="activites")
    # Champs
    type_activite = models.CharField(max_length=50, choices=TYPE_ACTIVITE_CHOICES, verbose_name="Type d'activité")
    date_activite = models.DateField(verbose_name="Date de l'activité", default=date.today)
    heure_debut = models.TimeField(verbose_name="Heure de début", null=True, blank=True)
    heure_fin = models.TimeField(verbose_name="Heure de fin", null=True, blank=True)
    description = models.TextField(verbose_name="Description détaillée", blank=True, null=True)
    lieu = models.CharField(max_length=20, verbose_name="Lieu", blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, verbose_name="Statut", default='planifie')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")

    class Meta:
        db_table = 'activites_activite'
        verbose_name = "Activité"
        verbose_name_plural = "Activités"
        ordering = ['-date_activite', 'heure_debut']

    def __str__(self):
        return f"{self.get_type_activite_display()} - {self.date_activite}"

# La fonction pour calculer la duree estimée pour l'activité

    @property
    def duree_activite(self):
        if self.heure_debut and self.heure_fin:
            debut = datetime.combine(self.date_activite, self.heure_debut)
            fin = datetime.combine(self.date_activite, self.heure_fin)

            duree = fin - debut

            heures = duree.seconds // 3600
            minutes = (duree.seconds % 3600) // 60

            return f"{heures}h {minutes}min"
        return "Non définie"