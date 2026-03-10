from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from . import views
from django.urls import reverse_lazy

app_name = 'users'

urlpatterns = [
    # Authentification
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # Profil
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/modifier/', views.modifier_profile, name='modifier_profile'),

    # Admin
    path('users/', views.list_utilisateurs, name='liste_utilisateurs'),
    path('valider-utilisateur/<int:user_id>/', views.valider_utilisateur, name ='valider_utilisateur'),
    path('supprimer-utilisateur/<int:user_id>/', views.soft_delete_utilisateur, name='supprimer_utilisateur'),

    # Password reset
    path('password_reset/', views.password_reset_request, name='password_reset_request'),
    path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    path('reset/<uuid:token>/', views.password_reset_confirm, name='password_reset_confirm'),

    
]