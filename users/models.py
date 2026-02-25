from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from techniciens.models import Technicien
from commercials.models import Commercial
from django.conf import settings


class User(AbstractUser):
    """Modèle utilisateur personnalisé"""

    # Types d'utilisateurs
    TYPE_USER = [
        ('admin', 'Administrateur'),
        ('superviseur', 'Superviseur'),
        ('commercial', 'Commercial'),
        ('technicien', 'Technicien'),
        ('comptable', 'Comptable'),
    ]

    # Champs supplémentaires
    #user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    user_type = models.CharField(max_length=20, choices=TYPE_USER)
    #user_type = models.CharField(max_length=20, choices=TYPE_USER, default='technicien')
    nom = models.CharField(max_length=25,blank=True)
    prenom = models.CharField(max_length=30,blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.TextField(blank=True)
    photo = models.ImageField(upload_to='users/photos/', null=True, blank=True)

    # Dates
    date_inscription = models.DateTimeField(auto_now_add=True)
    derniere_connexion = models.DateTimeField(null=True, blank=True)

    # Statut
    est_actif = models.BooleanField(default=True)
    est_valide = models.BooleanField(default=False, help_text="Compte validé par un admin")

    # ✅ CORRECTION: Utiliser les classes importées directement
    technicien = models.OneToOneField(
        Technicien,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_account'
    )

    commercial = models.OneToOneField(
        Commercial,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_account'
    )

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return f"{self.username} - {self.get_full_name()} ({self.get_user_type_display()})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username