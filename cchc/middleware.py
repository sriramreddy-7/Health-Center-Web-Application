import time
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import logout


class SessionExpiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            current_activity = int(time.time())
            session_timeout = settings.SESSION_EXPIRE_SECONDS

            if last_activity and current_activity - last_activity > session_timeout:
                messages.warning(request, 'Your session has expired. Please log in again.')
                logout(request)
                return redirect(settings.LOGOUT_REDIRECT_URL)

            request.session['last_activity'] = current_activity

        response = self.get_response(request)
        return response
