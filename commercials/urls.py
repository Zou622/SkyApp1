# monapp/urls.py (dans votre dossier d'application)
from django.urls import path
from . import views

urlpatterns = [
    # URLs pour les commerciaux
    path('', views.list_commercial, name='list_commercial'),
    path('ajouter_commercial/', views.ajouter_commercial, name='ajouter_commercial'),
    path('commercial/<int:pk>/', views.detail_commercial, name='detail_commercial'),
    path('commercial/<int:pk>/modifier/', views.modifier_commercial, name='modifier_commercial'),
    path('commercial/<int:pk>/supprimer/', views.supprimer_commercial, name='supprimer_commercial'),

]