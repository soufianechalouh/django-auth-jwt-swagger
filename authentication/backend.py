import jwt
from django.contrib.auth.models import User
from rest_framework import authentication, exceptions
from django.conf import settings


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)

        if not auth_data:
            return None

        prefix, token = auth_data.decode("utf-8").split()

        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY)

            user = User.objects.get(username=payload["username"])

            return user, token

        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed("Invalid token")
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expired")
        except Exception as e:
            print("Uncaught auth exception")
            print(e)

        return super().authenticate(request)
