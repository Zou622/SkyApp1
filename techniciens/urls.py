from django.urls import path
from . import views

urlpatterns = [

    # URLs pour les techniciens
    path('list_technicien', views.list_technicien, name='list_technicien'),

    path('ajouter_technicien/', views.ajouter_technicien, name='ajouter_technicien'),
    path('enregistrer_technicien/', views.enregistrer_technicien, name='enregistrer_technicien'),
    path('technicien/<int:technicien_id>/', views.detail_technicien, name='detail_technicien'),
    path('modifier_technicien/<int:technicien_id>/', views.modifier_technicien, name='modifier_technicien'),
    path('supprimer_technicien/<int:technicien_id>/', views.supprimer_technicien, name='supprimer_technicien'),

    
]