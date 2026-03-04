from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from . import views

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
    path('valider-utilisateur/<int:user_id>/', views.valider_utilisateur, name='valider_utilisateur'),
    path('supprimer-utilisateur/<int:user_id>/', views.soft_delete_utilisateur, name='supprimer_utilisateur'),

    # Password reset
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset/complete/',auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),



    

]