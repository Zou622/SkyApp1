from django.utils import timezone
from datetime import timedelta


class LastUserActivityMiddleware:
    """Middleware pour tracker la dernière activité"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            now = timezone.now()
            last_seen = request.session.get('last_seen')

            if not last_seen or (now - last_seen) > timedelta(minutes=5):
                request.user.derniere_connexion = now
                request.user.save()
                request.session['last_seen'] = now

        return self.get_response(request)

    # Crée un fichier middleware.py dans ton app users
    class DebugSessionMiddleware:
        def __init__(self, get_response):
            self.get_response = get_response

        def __call__(self, request):
            return self.get_response(request)

        def process_view(self, request, view_func, view_args, view_kwargs):
            if hasattr(request, 'session'):
                # Vérifie le contenu de la session
                for key, value in request.session.items():
                    if hasattr(value, 'year'):  # C'est probablement une date
                        print(f"⚠️ Date trouvée dans session[{key}] = {value}")
                        # Convertir en string pour éviter l'erreur
                        request.session[key] = value.isoformat()
            return None