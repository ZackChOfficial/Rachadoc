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
def get_user(headers):
    user = None
    token_key = None

    try:
        auth_key = headers["authorization"]
        _ = auth_key.split()
        token_key = _[1].strip()
    except KeyError or AttributeError:
        pass

    if token_key is not None and token_key != "":
        token = AccessToken.objects.get(token=token_key)
        token_valid = token.is_valid()
        if token_valid:
            user = token.user

    return user or AnonymousUser()


@database_sync_to_async
def get_clinic(headers, user):
    clinic_id = None

    try:
        clinic_id = headers["clinic"]
    except KeyError or AttributeError:
        pass
    if not clinic_id or not Clinic.objects.filter(id=clinic_id).exists():
        return None
    if user:
        profile = get_user_profile(user)
        if profile == settings.SUPERUSER:
            return clinic_id
        elif profile == settings.DOCTOR:
            doctor = Doctor.objects.get(id=user.id)
            if doctor.clinics.filter(id=clinic_id).exists():
                return clinic_id
        elif profile == settings.RECEPTIONIST:
            recept = Receptionist.objects.get(id=user.id)
            if recept.clinic.id == int(clinic_id):
                return clinic_id
    return None


class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        headers = {}
        for param in scope.get("headers"):
            key = param[0].decode()
            value = param[1].decode()
            headers[key] = value
        scope["user"] = await get_user(headers)
        scope["clinic"] = await get_clinic(headers, scope["user"])
        return await super().__call__(scope, receive, send)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
