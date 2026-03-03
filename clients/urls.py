from django.urls import path

from users.urls import app_name
from . import views

app_name = 'clients'

urlpatterns = [
    path('',views.acceuil),
    path('list_client/', views.list_client, name= 'list_client'),
    path('ajouter_client/', views.enregistrer_client, name='ajouter_client'),
    path('afficher_formulaire/', views.afficher_formulaire_ajout, name='afficher_formulaire'),
    path('enregistrer_client/', views.enregistrer_client, name='enregistrer_client'),
    path('client/<int:client_id>/', views.detail_client, name='detail_client'),
    path('modifier_client/<int:client_id>/', views.modifier_client, name='modifier_client'),
    path('supprimer_client/<int:client_id>/', views.supprimer_client, name='supprimer_client'),
    path('client/<int:client_id>/pdf/', views.voir_pdf, name='voir_pdf'),
    path('client/<int:client_id>/activate/', views.activate_client, name='activate_client'),

   # URLS du module activité
    path('activites/', views.list_activite, name='list_activite'),
    path('activite/ajouter/client/<int:client_id>/', views.ajouter_activite_avec_client,name='ajouter_activite_avec_client'),

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
    path("mes-activites/", views.mes_activites, name="mes_activites"),
    path('activite/<int:pk>/rapport/', views.rapport_activite, name='rapport_activite'),


]
