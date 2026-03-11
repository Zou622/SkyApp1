"""
skyApp/urls.py - Configuration des URLs principales
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentification et utilisateurs
    path('', include('users.urls')),

    # Applications métier
    path('', include('clients.urls')),
    path('', include('techniciens.urls')),
    path('', include('commercials.urls')),
    path('', include('activites.urls')),
    path('', include('rapportActivites.urls')),
    #path('',include('users.urls')),

]

# Ajout des fichiers médias et statiques en mode debug
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)