#!/usr/bin/env python3

from typing import Any, Optional, Self

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
            return ConfigDataAPIDir(self.api, f"{self.api_dir}").with_post()
        else:
            # Return the /rest/config/{folders,devices}/data_id
            return ConfigDataAPIDir(self.api, f"{self.api_dir}/{data_id}").with_patch().with_delete()


class ConfigDataAPIDir(APIDir):
    def __init__(self, api: API, api_dir: str) -> None:
        super().__init__(api, api_dir)
        self.has_post = False
        self.has_patch = False
        self.has_delete = False

    def with_patch(self) -> Self:
        self.has_patch = True
        return self

    def with_post(self) -> Self:
        self.has_post = True
        return self

    def with_delete(self) -> Self:
        self.has_delete = True
        return self

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
