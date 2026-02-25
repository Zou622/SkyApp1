from django.urls import path
from . import views

# Le nom de l'application pour les namespaces
app_name = 'activities'

urlpatterns = [
#path('activite/enregistrer/', views.enregistrer_activite, name='enregistrer_activite'),
    path('activite/ajouter/', views.ajouter_activite, name='ajouter_activite'),
    path('activites/calendrier/', views.calendrier_activites, name='calendrier_activites'),
    path('activites/aujourdhui/', views.activites_aujourdhui, name='activites_aujourdhui'),
    path('activite/<int:pk>/', views.detail_activite, name='detail_activite'),

    path('activite/<int:pk>/modifier/', views.modifier_activite, name='modifier_activite'),
    path('activite/<int:pk>/supprimer/', views.supprimer_activite, name='supprimer_activite'),

    path('client/<int:client_id>/activites/', views.liste_activites_client, name='liste_activites_client'),
    path('activites/aujourdhui/', views.activites_aujourdhui, name='activites_aujourdhui'),
    path('activites-par-technicien/', views.activites_par_technicien, name='activites_par_technicien'),


]