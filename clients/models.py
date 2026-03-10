from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from commercials.models import Commercial



TYPE_CONTRAT_CHOICES = [
        ('dedie', 'Dédié'),
        ('partage', 'Partagé'),
        ('symetrique', 'Symétrique'),
        ('asymetrique', 'Asymétrique'),
        ('autre', 'Autre'),
    ]


class Client(models.Model):
    commercial = models.ForeignKey(Commercial, on_delete=models.SET_NULL, null=True)
    nom_client = models.CharField(max_length=255)
    adresse = models.TextField(blank=True, null=True)
    quartier = models.CharField(max_length=100, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    vlan = models.CharField(max_length=10, blank=True, null=True)
    adresse_ip = models.GenericIPAddressField(blank=True, null=True)
    statut = models.CharField(max_length=20, default='non_actif')
    type_contrat = models.CharField(max_length=20, choices=TYPE_CONTRAT_CHOICES, blank=True, null=True)
    capacite = models.CharField(max_length=5, blank=True, null=True)
    download = models.CharField(max_length=5, blank=True, null=True)
    upload = models.CharField(max_length=5, blank=True, null=True)
    contrat_pdf = models.FileField(upload_to='contrats/', blank=True, null=True)



    def __str__(self):
        return self.nom_client
    

    # Fonctions de vérification des rôles
    def est_technicien(user):
        return hasattr(user, 'technicien')

    def est_admin(user):
        return user.is_superuser or user.is_staff

