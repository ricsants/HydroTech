from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken

from .models import Usuario


class APITokenAuthentication(authentication.BaseAuthentication):
    keyword = 'Bearer'

    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request).split()
        if not auth_header or auth_header[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth_header) == 1:
            raise AuthenticationFailed('Invalid token header. No credentials provided.')
        if len(auth_header) > 2:
            raise AuthenticationFailed('Invalid token header.')

        token = auth_header[1].decode('utf-8')
        try:
            user = Usuario.objects.get(api_token=token)
        except Usuario.DoesNotExist:
            # Let the other auth backends try (e.g. JWT)
            return None

        return (user, token)


class UsuarioJWTAuthentication(authentication.BaseAuthentication):
    """
    Auth JWT que NÃO depende de AUTH_USER_MODEL (django.contrib.auth.User).
    Busca o usuário no model local `usuarios.Usuario`.
    """
    keyword = 'Bearer'

    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request).split()
        if not auth_header or auth_header[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth_header) == 1:
            raise AuthenticationFailed('Invalid token header. No credentials provided.')
        if len(auth_header) > 2:
            raise AuthenticationFailed('Invalid token header.')

        raw_token = auth_header[1].decode('utf-8')

        try:
            validated_token = AccessToken(raw_token)
        except Exception:
            raise AuthenticationFailed('Token inválido ou expirado.')

        user_id = validated_token.get('user_id')
        if user_id is None:
            raise AuthenticationFailed('Token não contém identificação do usuário.')

        try:
            user = Usuario.objects.get(id=user_id)
        except Usuario.DoesNotExist:
            # Mantém o mesmo shape que você viu no frontend (code=user_not_found)
            raise AuthenticationFailed('User not found', code='user_not_found')

        return (user, raw_token)


class JWTOrAPITokenAuthentication(authentication.BaseAuthentication):
    """
    Tenta primeiro API token (api_token) e, se não encontrar, tenta JWT.
    """
    def authenticate(self, request):
        api_auth = APITokenAuthentication()
        api_result = api_auth.authenticate(request)
        if api_result:
            return api_result

        jwt_auth = UsuarioJWTAuthentication()
        return jwt_auth.authenticate(request)

    def authenticate_header(self, request):
        return 'Bearer'
