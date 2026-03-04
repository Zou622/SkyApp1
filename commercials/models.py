from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class Commercial(models.Model):

    user_account = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="commercial_profile"
    )

    SPECIALITES = [
        ('reseau', 'Réseau et Télécom'),
        ('vente', 'Vente et Marketing'),
        ('technique', 'Support Technique'),
        ('gestion', 'Gestion Clientèle'),
        ('autre', 'Autre'),
    ]

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)

    quartier = models.CharField(max_length=100, blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)

    specialite = models.CharField(
        max_length=50,
        choices=SPECIALITES,
        default='vente'
    )

    taux_commission = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=10.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    date_embauche = models.DateField(blank=True, null=True)

    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    est_actif = models.BooleanField(default=True)

    class Meta:
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.prenom} {self.nom}"