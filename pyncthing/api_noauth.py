#!/usr/bin/env python3

from .api import APIDir


class Noauth(APIDir):
    """Entrypoint class for the noauth Syncthing REST API."""

    def health(self) -> bool:
        return self._get("health").json()["status"] == "OK"
