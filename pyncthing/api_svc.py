#!/usr/bin/env python3

from typing import Dict, List, Any
from .api import APIDir


class Svc(APIDir):
    """Entrypoint class for the svc Syncthing REST API."""

    def deviceid(self, deviceid: str) -> str:
        return self._get("deviceid", params={"id": deviceid}).json()["id"]

    def lang(self) -> List[str]:
        return self._get("lang").json()

    def random_string(self) -> str:
        return self._get("random/string").json()["random"]

    def report(self) -> Dict[str, Any]:
        return self._get("report").json()
