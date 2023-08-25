#!/usr/bin/env python3

from typing import Any, Dict, Generator, List, Tuple

from .api import APIDir

PaginatedErrors = Tuple[List[Dict[str, str]], Tuple[int, int]]


class Folder(APIDir):
    """Entrypoint class for the folder Syncthing REST API."""

    def errors(self, folder: str) -> Generator[Dict[str, str], None, None]:
        for page in self._get_paginated("errors", {"folder": folder}):
            if not page["errors"]:
                return
            for error in page["errors"]:
                yield error

    def versions(self, folder: str) -> Dict[str, List[Dict[str, Any]]]:
        params = {"folder": folder}
        return self._get("errors", params=params).json()

    def versions_restore(self, folder: str, files: Dict[str, str]) -> None:
        params = {"folder": folder}
        self._post("errors", params=params, json=files)
