import time
from django.conf import settings
from django.core.cache import cache
from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split()[1]
            user = cache.get(token)
            if user is None:
                # If user is not in cache, authenticate and cache the user
                jwt_authenticator = JWTAuthentication()
                try:
                    validated_token = jwt_authenticator.get_validated_token(token)
                    user = jwt_authenticator.get_user(validated_token)
                    cache.set(token, user, timeout=settings.JWT_AUTH_CACHE_TIMEOUT)
                except Exception:
                    user = None

            request.user = user

        response = self.get_response(request)
        return response
