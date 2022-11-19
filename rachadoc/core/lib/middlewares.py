from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from oauth2_provider.models import AccessToken
from django.contrib.auth.models import AnonymousUser


@database_sync_to_async
def get_user(scope):
    user = None
    token_key = None

    headers = {}
    for param in scope.get("headers"):
        key = param[0].decode()
        value = param[1].decode()
        headers[key] = value

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


class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        scope["user"] = await get_user(scope)
        return await super().__call__(scope, receive, send)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
