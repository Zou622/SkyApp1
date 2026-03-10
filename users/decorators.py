from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def user_type_required(allowed_types):
    """Décorateur pour restreindre l'accès par type d'utilisateur"""

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "Vous devez être connecté")
                return redirect('users:login')

            if request.user.user_type not in allowed_types:
                messages.error(request, "Vous n'avez pas les permissions nécessaires")
                return redirect('users:dashboard')

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def admin_required(view_func):
    """Décorateur pour admin uniquement"""
    return user_type_required(['admin'])(view_func)


def technicien_required(view_func):
    """Décorateur pour technicien uniquement"""
    return user_type_required(['admin', 'technicien'])(view_func)


def commercial_required(view_func):
    """Décorateur pour commercial uniquement"""
    return user_type_required(['admin', 'commercial'])(view_func)