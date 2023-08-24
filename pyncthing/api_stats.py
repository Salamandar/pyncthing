#!/usr/bin/env python3

from typing import Dict, Any
from .api import APIDir


class Stats(APIDir):
    """Entrypoint class for the stats Syncthing REST API."""

    def device(self) -> Dict[str, Dict[str, Any]]:
        return self._get("device").json()

    def folder(self) -> Dict[str, Dict[str, Any]]:
        return self._get("folder").json()
