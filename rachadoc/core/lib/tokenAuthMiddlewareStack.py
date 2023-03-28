from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from oauth2_provider.models import AccessToken
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from core.lib.utils import get_user_profile
from clinic.models import Clinic
from accounts.models import Doctor, Receptionist


@database_sync_to_async
def get_user(params):
    user = None
    token_key = None

    try:
        token_key = params["token"]
    except KeyError or AttributeError:
        pass

    if token_key is not None and token_key != "":
        try:
            token = AccessToken.objects.get(token=token_key)
            token_valid = token.is_valid()
            if token_valid:
                user = token.user
        except AccessToken.DoesNotExist:
            pass
    return user or AnonymousUser()


@database_sync_to_async
def get_clinic(user):
    profile = get_user_profile(user)
    if profile == settings.DOCTOR:
        doctor = Doctor.objects.get(id=user.id)
        clinic = doctor.clinics.first()
        return str(clinic.id) if clinic else None
    elif profile == settings.RECEPTIONIST:
        recept = Receptionist.objects.get(id=user.id)
        return str(recept.clinic.id) if recept and recept.clinic else None
    return None


def query_string_to_dict(query_string: str):
    data = dict()
    if not query_string:
        return data
    params = query_string.split("&")
    for param in params:
        key_value = param.split("=")
        if len(key_value) == 2:
            data[key_value[0]] = key_value[1]
    return data


class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        if "query_string" in scope:
            query_string = scope.get("query_string").decode()
            data = query_string_to_dict(query_string)
            scope["user"] = await get_user(data)
            if "user" in scope:
                scope["clinic_id"] = await get_clinic(scope["user"])
        return await super().__call__(scope, receive, send)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
