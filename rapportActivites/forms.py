from django import forms
from .models import RapportActivite, Activite


class RapportActiviteForm(forms.ModelForm):
    class Meta:
        model = RapportActivite
        fields = [
            'date_intervention_reelle', 'heure_debut_reelle', 'heure_fin_reelle',
            'travaux_realises', 'difficultes_rencontrees', 'solutions_apportees',
            'etat_avant', 'etat_apres',
            'equipements_utilises', 'materiel_consomme', 'materiel_remplace',
            'parametres_configures', 'qualite_signal', 'debit_constate',
            'client_present', 'satisfaction_client', 'commentaire_client',
            'recommandations', 'prochaine_action', 'date_prochaine_intervention',
            'photo_avant', 'photo_apres', 'document_joint'
        ]
        widgets = {
            'date_intervention_reelle': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'heure_debut_reelle': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'heure_fin_reelle': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'travaux_realises': forms.Textarea(attrs={'rows': 4, 'class': 'form-control',
                                                      'placeholder': 'Décrivez en détail les travaux réalisés...'}),
            'difficultes_rencontrees': forms.Textarea(
                attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Avez-vous rencontré des difficultés ?'}),
            'solutions_apportees': forms.Textarea(
                attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Comment avez-vous résolu les problèmes ?'}),
            'etat_avant': forms.Textarea(
                attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'État du site avant intervention'}),
            'etat_apres': forms.Textarea(
                attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'État du site après intervention'}),
            'equipements_utilises': forms.Textarea(
                attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Liste des équipements utilisés'}),
            'materiel_consomme': forms.Textarea(attrs={'rows': 2, 'class': 'form-control',
                                                       'placeholder': 'Matériel consommé (câbles, connecteurs, etc.)'}),
            'materiel_remplace': forms.Textarea(
                attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Matériel remplacé'}),
            'parametres_configures': forms.Textarea(
                attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Paramètres modifiés/configurés'}),
            'qualite_signal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: -45dBm'}),
            'debit_constate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 50 Mbps'}),
            'client_present': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'satisfaction_client': forms.Select(attrs={'class': 'form-select'}),
            'commentaire_client': forms.Textarea(
                attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Commentaires du client'}),
            'recommandations': forms.Textarea(
                attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Recommandations pour le client'}),
            'prochaine_action': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ex: Maintenance préventive'}),
            'date_prochaine_intervention': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'photo_avant': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'photo_apres': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'document_joint': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.technicien = kwargs.pop('technicien', None)
        self.activite = kwargs.pop('activite', None)
        super().__init__(*args, **kwargs)

        # Pré-remplir avec les données de l'activité
        if self.activite:
            self.fields['date_intervention_reelle'].initial = self.activite.date_activite
            self.fields['heure_debut_reelle'].initial = self.activite.heure_debut
            self.fields['heure_fin_reelle'].initial = self.activite.heure_fin