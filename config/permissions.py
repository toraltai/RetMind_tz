import jwt
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class IsAuthenticatedViaJWT(BasePermission):
    message = 'Authentication via JWT failed'

    def has_permission(self, request, view):
        token = request.COOKIES.get('jwt')

        if not token:
            return False

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.DecodeError:
            raise AuthenticationFailed('Token is invalid')

        request.user = payload
        return True