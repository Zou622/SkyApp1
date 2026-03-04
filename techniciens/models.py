from django.db import models
from django.conf import settings

# SUPPRIMEZ cette ligne si elle existe
# from users.models import User

class Technicien(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    email = models.EmailField(verbose_name="Email", unique=True)
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")

    # Adresse
    quartier = models.CharField(max_length=100, verbose_name="Quartier")
    adresse = models.TextField(verbose_name="Adresse complète")

    # Photo
    photo = models.ImageField(
        upload_to='techniciens/photos/',
        verbose_name="Photo",
        blank=True,
        null=True
    )

    # Informations professionnelles
    specialite = models.CharField(
        max_length=100,
        verbose_name="Spécialité",
        blank=True
    )

    # Relation vers User (optionnelle - si vous voulez aussi un lien depuis Technicien)
    user = models.OneToOneField(
        'users.User',  # Utilisez une chaîne de caractères
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='technicien_profile'
    )

    # Statut
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('inactif', 'Inactif'),
        ('congé', 'En congé'),
        ('mission', 'En mission'),
    ]
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='actif',
        verbose_name="Statut"
    )
    est_actif = models.BooleanField(default=True)

    # Dates
    date_embauche = models.DateField(verbose_name="Date d'embauche")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

    def nom_complet(self):
        return f"{self.nom} {self.prenom}"

    def get_photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        return '/static/images/default-avatar.png'

    class Meta:
        verbose_name = "Technicien"
        verbose_name_plural = "Techniciens"
        ordering = ['nom', 'prenom']