"""Declares :class:`IClient`."""
from ckms.jose.models import JSONWebKeySet


class IClient:
    """The base interface of all headless client implementations."""

    async def get_server_time(self) -> int:
        """Return an integer indicating the server time, in seconds since
        the UNIX epoch.
        """
        raise NotImplementedError

    async def get_server_jwks(self) -> JSONWebKeySet:
        """Lookup the JSON Web Key Set (JWKS) published by the
        remote peer to encrypt sent data and verify signatures
        created by it.
        """
        raise NotImplementedError