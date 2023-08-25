#!/usr/bin/env python3

from typing import Dict, List, Any, Optional, Generator, Tuple
from .api import APIDir


class DB(APIDir):
    """Entrypoint class for the db Syncthing REST API."""

    def browse(self, folder: str, levels: Optional[int], prefix: Optional[str]) -> List[Dict[str, Any]]:
        params = self.autoparams(folder=folder, levels=levels, prefix=prefix)
        return self._get("browse", params=params).json()

    def completion(self, folder: Optional[str], device: Optional[str]) -> Dict[str, Any]:
        params = self.autoparams(folder=folder, device=device)
        return self._get("completion", params=params).json()

    def file(self, folder: str, file: str) -> Dict[Any, Any]:
        params = {"folder": folder, "file": file}
        return self._get("file", params=params).json()

    def ignores(self, folder: str) -> Dict[str, List[str]]:
        params = {"folder": folder}
        return self._get("ignores", params=params).json()

    def ignores_post(self, folder: str, ignore: List[str]) -> Dict[str, List[str]]:
        params = {"folder": folder}
        return self._post("ignores", params=params, json=ignore).json()

    def localchanged(self, folder: str) -> Generator[Dict[str, Any], None, None]:
        for page in self._get_paginated("localchanged", {"folder": folder}):
            if not page["files"]:
                return
            for file in page["files"]:
                yield file

    def need(self, folder: str) -> Generator[Tuple[str, Dict[str, Any]], None, None]:
        """
        Returns a generator that yields a tuple(state, file)
        where state is "progress", "queued" or "rest"
        """
        arrays = ["progress", "queued", "rest"]
        for page in self._get_paginated("need", {"folder": folder}):
            empty = all(len(page[array]) == 0 for array in arrays)
            if empty:
                return
            for array in arrays:
                for file in page[array]:
                    yield array, file

    def override(self, folder: str) -> None:
        params = {"folder": folder}
        self._post("override", params=params)

    def prio(self, folder: str, file: str) -> None:
        params = {"folder": folder, "file": file}
        self._post("prio", params=params)

    def remoteneed(self, folder: str, device: str) -> Generator[Dict[str, Any], None, None]:
        params = {"folder": folder, "device": device}
        for page in self._get_paginated("remoteneed", params):
            if not page["files"]:
                return
            for file in page["files"]:
                yield file

    def revert(self, folder: str) -> None:
        params = {"folder": folder}
        self._post("revert", params=params)

    def scan(self, folder: str, sub: str) -> None:
        params = self.autoparams(folder=folder, sub=sub)
        self._post("scan", params=params)

    def status(self, folder: str) -> Dict[str, Any]:
        params = {"folder": folder}
        return self._get("status", params=params).json()
