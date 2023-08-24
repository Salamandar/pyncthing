#!/usr/bin/env python3

from typing import Dict, Tuple, List, Any

from .api import API, APIDir

PaginatedErrors = Tuple[List[Dict[str, str]], Tuple[int, int]]


class Cluster(APIDir):
    """Entrypoint class for the cluster Syncthing REST API."""

    def __init__(self, api: API, api_dir: str):
        """Initialize the client."""
        super().__init__(api, api_dir)
        self._pending = ClusterPending(self.api, f"{self.api_dir}/pending")

    @property
    def pending(self):
        return self._pending


class ClusterPending(APIDir):
    """Entrypoint class for the cluster/pending Syncthing REST API."""

    def devices(self) -> Dict[str, Dict[str, str]]:
        return self._get("devices").json()

    def devices_del(self, device: str) -> None:
        self._delete("devices", params={"device": device})

    def folders(self) -> Dict[str, Any]:
        return self._get("folders").json()

    def folders_del(self, folder: str, device: str) -> None:
        params = {"folder": folder, "device": device}
        self._delete("folders", params=params)
