import jwt

from django.conf import settings

from rest_framework import authentication, exceptions

from .models import User, BlacklistedToken

class JWTAuthentication(authentication.BaseAuthentication): # NOQA
    """ JWTAuthenticattion implement authentication
        of token  received from the 'Authorization' Headers by
        the keyword 'Token'"""

    # initializing the token as an empty string
    keyword = 'Token'

    def authenticate(self, request):
        request.user = None

        # returns Authorization header
        # as a bytestring

        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header or auth_header[0].decode().lower() != self.keyword.lower():
            return None

        if len(auth_header) == 1:
                raise exceptions.AuthenticationFailed('Invalid token header. No credentials provided.')
        elif len(auth_header) > 2:
            raise exceptions.AuthenticationFailed('Invalid token header. Token string should not contain spaces.')
        return self.authenticate_credentials(request, auth_header[1].decode())

    def authenticate_credentials(self, request, token): # NOQA
        """
        authenticate the given credentials. If authentication is
        successful, return the user and token. If not, throw an error.
        """

        if BlacklistedToken.objects.filter(token=token).first():
                raise exceptions.AuthenticationFailed('Token is blacklisted')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except Exception as e:
            if e.__class__.__name__ == 'DecodeError':
                raise exceptions.AuthenticationFailed('Cannot decode token')
            elif e.__class__.__name__ == "ExpiredSignatureError":
                raise exceptions.AuthenticationFailed('Token has expired')
            else:
                raise exceptions.AuthenticationFailed(str(e))

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No user Found')
        if not user.is_active:
            raise exceptions.AuthenticationFailed('User has been deactivated')

        return user, token
