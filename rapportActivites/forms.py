from django import forms

from rapportActivites.models import RapportActivite


class RapportActiviteForm(forms.ModelForm):

    class Meta:
        model = RapportActivite
        fields = [
            'date_intervention_reelle',
            'heure_debut_reelle',
            'heure_fin_reelle',
            'travaux_realises',
            'difficultes_rencontrees',
            'solutions_apportees',
            'etat_avant',
            'etat_apres',
            'equipements_utilises',
            'materiel_consomme',
            'materiel_remplace',
            'parametres_configures',
            'qualite_signal',
            'debit_constate',
            'client_present',
            'satisfaction_client',
            'commentaire_client',
            'recommandations',
            'prochaine_action',
            'date_prochaine_intervention',
            'photo_avant',
            'photo_apres',
            'document_joint'
        ]

    def __init__(self, *args, **kwargs):

        self.activite = kwargs.pop('activite', None)  # IMPORTANT

        super().__init__(*args, **kwargs)

        if self.activite:

            self.fields['date_intervention_reelle'].initial = self.activite.date_activite
            self.fields['heure_debut_reelle'].initial = self.activite.heure_debut
            self.fields['heure_fin_reelle'].initial = self.activite.heure_fin

            type_activite = self.activite.type_activite

            champs_par_type = {

                "installation": [
                    'date_intervention_reelle',
                    'heure_debut_reelle',
                    'heure_fin_reelle',
                    'travaux_realises',
                    'equipements_utilises',
                    'parametres_configures',
                    'photo_avant',
                    'photo_apres'
                ],

                "maintenance": [
                    'date_intervention_reelle',
                    'heure_debut_reelle',
                    'heure_fin_reelle',
                    'travaux_realises',
                    'materiel_remplace',
                    'solutions_apportees',
                    'photo_avant',
                    'photo_apres'
                ],

                "survey": [
                    'date_intervention_reelle',
                    'travaux_realises',
                    'etat_avant',
                    'difficultes_rencontrees',
                    'photo_avant'
                ],

                "investigation": [
                    'date_intervention_reelle',
                    'travaux_realises',
                    'difficultes_rencontrees',
                    'solutions_apportees'
                ]
            }

            champs_autorises = champs_par_type.get(type_activite, [])

            for field in list(self.fields.keys()):
                if field not in champs_autorises:
                    self.fields.pop(field)