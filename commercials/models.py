from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Commercial(models.Model):
    SPECIALITES = [
        ('reseau', 'Réseau et Télécom'),
        ('vente', 'Vente et Marketing'),
        ('technique', 'Support Technique'),
        ('gestion', 'Gestion Clientèle'),
        ('autre', 'Autre'),
    ]

    # Informations personnelles
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")

    # Coordonnées
    quartier = models.CharField(max_length=100, verbose_name="Quartier", blank=True, null=True)
    adresse = models.TextField(verbose_name="Adresse complète", blank=True, null=True)
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    email = models.EmailField(verbose_name="Adresse email", blank=True, null=True)

    # Informations professionnelles
    specialite = models.CharField(
        max_length=50,
        choices=SPECIALITES,
        verbose_name="Spécialité",
        default='vente'
    )
    taux_commission = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Taux de commission (%)",
        default=10.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    date_embauche = models.DateField(verbose_name="Date d'embauche", blank=True, null=True)

    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    est_actif = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        verbose_name = "Commercial"
        verbose_name_plural = "Commerciaux"
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    def nom_complet(self):
        return f"{self.prenom} {self.nom}"

    def anciennete(self):
        if self.date_embauche:
            from datetime import date
            today = date.today()
            return today.year - self.date_embauche.year - (
                    (today.month, today.day) < (self.date_embauche.month, self.date_embauche.day)
            )
        return 0