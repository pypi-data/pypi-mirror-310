import hashlib
import hmac
from base64 import b64encode

from onoffice.actions import Action
from onoffice.resources import Resource


def create_hmac(token: str, secret: str, timestamp: int, resource: Resource, action: Action, encoding="utf-8"):
    """Creates a base 64 encoding string based on a list of fields that is encrypted with SHA265."""
    fields = [str(timestamp), token, resource.value, action.value]

    salt = hmac.new(
        bytes(secret, encoding=encoding),
        bytes("".join(fields), encoding=encoding),
        digestmod=hashlib.sha256,
    ).digest()

    return b64encode(salt).decode(encoding)
