#!/usr/bin/env python3
"""Entrypoint for the system Syncthing REST API."""

from typing import Optional, List, Dict, Any

from .api import APIDir


class System(APIDir):
    """Entrypoint class for the system Syncthing REST API."""

    def browse(self, current: Optional[str] = None) -> List[str]:
        params = self.autoparams(current=current)
        return self._get("browse", params=params).json()

    def connections(self) -> Dict[str, Any]:
        return self._get("connections").json()

    def debug(self) -> Dict[str, Any]:
        return self._get("debug").json()

    def debug_post(self, enable: Optional[List[str]] = None, disable: Optional[List[str]] = None) -> None:
        params = {}
        if enable:
            params["enable"] = ",".join(enable)
        if disable:
            params["disable"] = ",".join(disable)
        self._post("debug", params=params)

    def discovery(self) -> Dict[str, List[str]]:
        return self._get("discovery").json()

    def error(self) -> List[Dict[str, str]]:
        return self._get("error").json()["errors"]

    def error_post(self, text: str) -> None:
        self._post("error", data=text)

    def error_clear(self) -> None:
        self._post("error/clear")

    def log(self) -> List[Dict[str, str]]:
        return self._get("log").json()["messages"]

    def log_txt(self) -> str:
        return self._get("log.txt").text

    def paths(self) -> Dict[str, str]:
        return self._get("paths").json()

    def pause(self, device_id: Optional[str] = None) -> None:
        self._post("pause", params=self.autoparams(device=device_id))

    def ping(self):
        """Check server availability."""
        res = self._get("ping").json()
        expected = {"ping": "pong"}
        if res != expected:
            raise RuntimeError(f"ping result is {res} instead of {expected}")

    def reset(self, folder: Optional[str] = None) -> None:
        self._post("reset", params=self.autoparams(folder=folder))

    def restart(self) -> None:
        self._post("restart")

    def resume(self, device_id: Optional[str] = None) -> None:
        self._post("resume", params=self.autoparams(device=device_id))

    def shutdown(self) -> None:
        self._post("shutdown")

    def status(self) -> Dict[str, Any]:
        return self._get("status").json()

    def upgrade(self) -> Dict[str, Any]:
        return self._get("upgrade").json()

    def upgrade_perform(self) -> None:
        self._post("upgrade")

    def version(self) -> Dict[str, str]:
        return self._get("version").json()


# FIXME: handle standard errors as notfound
