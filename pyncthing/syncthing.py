#!/usr/bin/env python3
"""
Entrypoint for the Syncthing REST API.
"""

from .api import API, APIDir
from .api_cluster import Cluster
from .api_config import Config
from .api_db import DB
from .api_debug import Debug
from .api_events import Events
from .api_folder import Folder
from .api_noauth import Noauth
from .api_stats import Stats
from .api_svc import Svc
from .api_system import System


class Syncthing:
    """Entrypoint class."""

    def __init__(self, *args, **kwargs):
        """Initialize the client."""
        self._api = API(*args, **kwargs)

        self.endpoints = {
            "system": System(self._api, "system"),
            "config": Config(self._api, "config"),
            "cluster": Cluster(self._api, "cluster"),
            "folder": Folder(self._api, "folder"),
            "db": DB(self._api, "db"),
            "events": Events(self._api, "events"),
            "noauth": Noauth(self._api, "noauth"),
            "stats": Stats(self._api, "stats"),
            "svc": Svc(self._api, "svc"),
            "debug": Debug(self._api, "debug"),
        }

    def set_api_key(self, api_key: str) -> None:
        self._api.set_api_key(api_key)

    def __getattr__(self, attr) -> APIDir:
        if attr not in self.endpoints:
            raise RuntimeError(f"Unknown API point {attr}")
        return self.endpoints[attr]

    def close(self):
        """Close open client session."""
        # self._api.close()
