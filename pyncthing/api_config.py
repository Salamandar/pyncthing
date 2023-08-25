#!/usr/bin/env python3

from typing import Any, Optional

from .api import API, APIDir


class Config(APIDir):
    """Entrypoint class for the config Syncthing REST API."""

    def __call__(self, config: Optional[Any] = None) -> Any:
        if config:
            return self._put("", json=config)
        else:
            return self._get("")

    def restart_required(self) -> bool:
        return self._get("restart-required").json()["requiresRestart"]

    @property
    def folders(self):
        return ConfigAPIDir(self.api, f"{self.api_dir}/folders")

    @property
    def devices(self):
        return ConfigAPIDir(self.api, f"{self.api_dir}/devices")


class ConfigAPIDir(APIDir):
    """
    Entrypoint class for the config/folders and config/devices REST API.
    """

    def __call__(self, data_id: Optional[str] = None) -> Any:
        if data_id is None:
            # Return the /rest/config/{folders,devices}
            return ConfigDataAPIDir(self.api, f"{self.api_dir}", True, False, False)
        else:
            # Return the /rest/config/{folders,devices}/data_id
            return ConfigDataAPIDir(self.api, f"{self.api_dir}/{data_id}", False, True, True)


class ConfigDataAPIDir(APIDir):
    def __init__(self, api: API, api_dir: str, has_post: bool, has_patch: bool, has_delete: bool) -> None:
        super().__init__(api, api_dir)
        self.has_post = has_post
        self.has_patch = has_patch
        self.has_delete = has_delete

    def get(self) -> Any:
        return self._get("").json()

    def put(self, data: Any) -> Any:
        return self._put("", json=data)

    def post(self, data: Any) -> Any:
        if not self.has_post:
            raise RuntimeError(f"Invalid method on API path {self.api_dir}")
        return self._post("", json=data)

    def patch(self, data: Any) -> Any:
        if not self.has_patch:
            raise RuntimeError(f"Invalid method on API path {self.api_dir}")
        return self._patch("", json=data)

    def delete(self) -> Any:
        if not self.has_delete:
            raise RuntimeError(f"Invalid method on API path {self.api_dir}")
        return self._delete("")
