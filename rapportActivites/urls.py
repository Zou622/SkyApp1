from django.urls import path

from users.urls import app_name
from . import views

app_name = 'rapportActivites'

urlpatterns = [
    path('activites/technicien/<int:technicien_id>/', views.liste_activites_technicien, name='liste_activites_technicien_avec_id'),
    path('activites/technicien/', views.liste_activites_technicien, name='liste_activites_technicien'),
    path('activite/<int:activite_id>/demarrer/', views.demarrer_activite, name='demarrer_activite'),
    #path('activite/<int:activite_id>/rapport/creer/', views.creer_rapport_activite, name='creer_rapport_activite'),
    path("rapport/<int:activite_id>/", views.creer_rapport, name="creer_rapport"),
    #path('rapport/<int:rapport_id>/', views.detail_rapport, name='detail_rapport'),

]