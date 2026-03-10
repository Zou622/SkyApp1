from django.contrib.auth import logout
from django.shortcuts import redirect
from functools import wraps
# clients/decorators.py
from django.http import HttpResponseForbidden
from functools import wraps



def technicien_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):

        # Vérifie si l'utilisateur est connecté
        if not request.user.is_authenticated:
            return redirect('users:login')

        # Vérifie si l'utilisateur est technicien
        if not hasattr(request.user, 'technicien'):
            logout(request)  # 🔥 Déconnexion
            return redirect('users:login')  # 🔥 Redirection vers login

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('users:login')

        if not request.user.is_superuser:
            logout(request)  # 🔥 Déconnexion
            return redirect('users:login')

        return view_func(request, *args, **kwargs)

    return _wrapped_view



def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Vérifiez d'abord si l'utilisateur est authentifié
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Vous devez être connecté")
            
            # Vérifiez le rôle - ajoutez des prints pour déboguer
            print(f"Utilisateur: {request.user.username}")
            print(f"Rôle utilisateur: {getattr(request.user, 'role', 'Non défini')}")
            print(f"Rôles autorisés: {allowed_roles}")
            
            # Vérifiez si l'utilisateur a le bon rôle
            user_role = getattr(request.user, 'role', None)
            if user_role is not None and user_role in allowed_roles:
                return view_func(request, *args, **kwargs)
            
            # Si pas autorisé
            return HttpResponseForbidden(
                f"Accès refusé. Rôle requis: {', '.join(allowed_roles)}"
            )
        return _wrapped_view
    
    return decorator