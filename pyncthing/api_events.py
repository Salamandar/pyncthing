#!/usr/bin/env python3

from typing import Any, Generator
import requests
from urllib3.exceptions import ReadTimeoutError


from .api import API, APIDir


class Events(APIDir):
    """Entrypoint class for the events Syncthing REST API."""

    def __init__(self, api: API, api_dir: str):
        """Initialize the client."""
        super().__init__(api, api_dir)
        self._last_seen_id = 0
        self._timeout = 30
        self._running = False

    @property
    def last_seen_id(self):
        """Get last seen event's id."""
        return self._last_seen_id

    def start(self):
        self._running = True

    def stop(self):
        self._running = False

    def __call__(self) -> Generator[Any, None, None]:
        self._last_seen_id = 0
        self._running = True

        while self._running:
            try:
                params = {"since": self._last_seen_id}
                events = self._get("", params=params, timeout=self._timeout
                                   ).json()
                for event in events:
                    yield event
                self._last_seen_id = events[-1]["id"]
            except requests.exceptions.ConnectionError as err:
                if isinstance(err.args[0], ReadTimeoutError):
                    continue
                raise
