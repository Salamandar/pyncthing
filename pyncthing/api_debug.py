#!/usr/bin/env python3

from typing import Any
from .api import APIDir


class Debug(APIDir):
    """Entrypoint class for the debug Syncthing REST API."""

    # pylint: disable-next=invalid-name
    def peerCompletion(self) -> Any:
        return self._get("peerCompletion").json()

    def httpmetrics(self) -> Any:
        return self._get("httpmetrics").json()

    def cpuprof(self) -> Any:
        return self._get("cpuprof", timeout=35).content

    def heapprof(self) -> Any:
        return self._get("heapprof").content

    def support(self) -> Any:
        return self._get("support").content

    def file(self, folder: str, file: str) -> Any:
        params = {"folder": folder, "file": file}
        return self._get("file", params=params).json()
