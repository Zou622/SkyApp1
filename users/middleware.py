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