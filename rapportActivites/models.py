from django.db import models
from datetime import date, datetime
from techniciens.models import Technicien
from clients.models import Client
from django.contrib.auth.models import User
from activites.models import Activite
from django.conf import settings


class RapportActivite(models.Model):
    # Types de rapports (correspond à vos types d'activité)
    TYPE_RAPPORT_CHOICES = [
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

    STATUT_RAPPORT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('soumis', 'Soumis'),
        ('valide', 'Validé'),
        ('rejete', 'Rejeté'),
    ]

    # Lien avec l'activité (One-to-One car une activité n'a qu'un rapport)
    activite = models.OneToOneField(
        'activites.Activite',
        on_delete=models.CASCADE,
        related_name='rapport',
        verbose_name="Activité concernée"
    )

    # Auteur du rapport (technicien)
    technicien = models.ForeignKey(
        Technicien,
        on_delete=models.CASCADE,
        related_name='rapports_activites',
        verbose_name="Technicien"
    )

    # Dates
    date_rapport = models.DateTimeField(auto_now_add=True, verbose_name="Date de création du rapport")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    date_intervention_reelle = models.DateField(verbose_name="Date réelle d'intervention", default=date.today)
    heure_debut_reelle = models.TimeField(verbose_name="Heure début réelle", null=True, blank=True)
    heure_fin_reelle = models.TimeField(verbose_name="Heure fin réelle", null=True, blank=True)

    # Travaux réalisés
    travaux_realises = models.TextField(verbose_name="Travaux réalisés")
    difficultes_rencontrees = models.TextField(verbose_name="Difficultés rencontrées", blank=True)
    solutions_apportees = models.TextField(verbose_name="Solutions apportées", blank=True)

    # État du client
    etat_avant = models.TextField(verbose_name="État avant intervention")
    etat_apres = models.TextField(verbose_name="État après intervention")

    # Équipements
    equipements_utilises = models.TextField(verbose_name="Équipements utilisés", blank=True)
    materiel_consomme = models.TextField(verbose_name="Matériel consommé", blank=True)
    materiel_remplace = models.TextField(verbose_name="Matériel remplacé", blank=True)

    # Informations techniques
    parametres_configures = models.TextField(verbose_name="Paramètres configurés", blank=True)
    qualite_signal = models.CharField(max_length=50, verbose_name="Qualité du signal", blank=True)
    debit_constate = models.CharField(max_length=50, verbose_name="Débit constaté", blank=True)

    # Satisfaction client
    client_present = models.BooleanField(default=True, verbose_name="Client présent")
    satisfaction_client = models.IntegerField(
        choices=[(1, '1 - Très insatisfait'), (2, '2 - Insatisfait'),
                 (3, '3 - Moyen'), (4, '4 - Satisfait'), (5, '5 - Très satisfait')],
        null=True, blank=True,
        verbose_name="Satisfaction client"
    )
    commentaire_client = models.TextField(verbose_name="Commentaire client", blank=True)

    # Recommandations
    recommandations = models.TextField(verbose_name="Recommandations", blank=True)
    prochaine_action = models.CharField(max_length=200, verbose_name="Prochaine action", blank=True)
    date_prochaine_intervention = models.DateField(null=True, blank=True, verbose_name="Date prochaine intervention")

    # Photos et documents
    photo_avant = models.ImageField(upload_to='rapports/photos/avant/', null=True, blank=True,
                                    verbose_name="Photo avant")
    photo_apres = models.ImageField(upload_to='rapports/photos/apres/', null=True, blank=True,
                                    verbose_name="Photo après")
    document_joint = models.FileField(upload_to='rapports/documents/', null=True, blank=True,
                                      verbose_name="Document joint")

    # Validation
    statut = models.CharField(max_length=20, choices=STATUT_RAPPORT_CHOICES, default='brouillon', verbose_name="Statut")
    valide_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='rapports_valides',
        verbose_name="Validé par"
    )
    date_validation = models.DateTimeField(null=True, blank=True, verbose_name="Date de validation")
    commentaire_validation = models.TextField(verbose_name="Commentaire de validation", blank=True)

    class Meta:
        db_table = 'activites_rapport'
        verbose_name = "Rapport d'activité"
        verbose_name_plural = "Rapports d'activités"
        ordering = ['-date_rapport']

    def __str__(self):
        return f"Rapport {self.get_type_activite_display()} - {self.activite.client.nom_client} - {self.date_intervention_reelle}"

    @property
    def get_type_activite_display(self):
        """Récupère le type d'activité depuis l'activité liée"""
        return self.activite.get_type_activite_display()

    @property
    def duree_reelle(self):
        """Calcule la durée réelle de l'intervention"""
        if self.heure_debut_reelle and self.heure_fin_reelle:
            debut = datetime.combine(self.date_intervention_reelle, self.heure_debut_reelle)
            fin = datetime.combine(self.date_intervention_reelle, self.heure_fin_reelle)
            duree = fin - debut
            heures = duree.seconds // 3600
            minutes = (duree.seconds % 3600) // 60
            return f"{heures}h {minutes}min"
        return "Non définie"