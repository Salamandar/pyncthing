#!/usr/bin/env python3

from typing import Optional, Dict, Any, Generator
import requests
# import logging


class API():
    """Low level client."""

    def __init__(self, host: str) -> None:
        self.host = host
        self.api_key: Optional[str] = None

    def set_api_key(self, api_key: str) -> None:
        self.api_key = api_key

    def request(self, path: str, method: str = "", **kwargs):
        # logging.warning("requests %s %s", method, path)

        # Compose the kwargs to requests (could be overriden from apidirs)
        # But we want the API Key always here.
        final_kwargs: Dict[str, Any] = {
            "timeout": 10,
            "headers": {}
        }
        final_kwargs.update(kwargs)
        if final_kwargs.get("apikey", True):
            final_kwargs["headers"].update({"X-API-Key": self.api_key})

        url = f"{self.host}/{path}"
        try:
            response = requests.request(method, url, **final_kwargs)
        except Exception as err:
            err.add_note(f"While accessing {url}")
            raise

        try:
            response.raise_for_status()
        except Exception as err:
            text = response.text
            err.add_note(text)
            self.requestprint(response.request)
            raise
        return response

    def requestprint(self, req) -> None:
        print('{}\n{}\r\n{}\r\n\r\n{}'.format(
            '-----------START-----------',
            req.method + ' ' + req.url,
            '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            req.body,
        ))


class APIDir():
    def __init__(self, api: API, api_dir: str) -> None:
        self.api: API = api
        self.api_dir: str = api_dir

    def autoparams(self, **kwargs):
        return {key: value for key, value in kwargs.items() if value is not None}

    def _request(self, path: str, method: str = "", **kwargs):
        return self.api.request(f"{self.api_dir}/{path}", method=method, **kwargs)

    def _get(self, path, **kwargs):
        return self._request(path, **kwargs, method="GET")

    def _post(self, path, **kwargs):
        return self._request(path, **kwargs, method="POST")

    def _put(self, path, **kwargs):
        return self._request(path, **kwargs, method="PUT")

    def _patch(self, path, **kwargs):
        return self._request(path, **kwargs, method="PATCH")

    def _delete(self, path, **kwargs):
        return self._request(path, **kwargs, method="DELETE")

    def _get_paginated(self, path, general_params: Dict[str, Any]) -> Generator[Dict[Any, Any], None, None]:
        next_page = 0
        while True:
            params = general_params | {"page": next_page}
            result = self._get(path, params=params).json()
            # Should be the same as next_page++
            next_page = result["page"] + 1
            yield result
