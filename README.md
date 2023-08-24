# Pyncthing

This is a `requests`-based API client for Syncthing.

It's fully compatible with Syncthing v1.23.7.

Please see the full documentation on <https://docs.syncthing.net/dev/rest>.

## Why ?

This project aims to write a simple and clean API client for desktop clients.
It might be used as a backend for Syncthing-GTK in the near future.

There are 2 packages already existing: <https://github.com/zhulik/aiosyncthing>
(a huge inspiration) and <https://github.com/blakev/python-syncthing>.
But they are dead projects and not up to date (they don't support the PATCH API).


## Installation

TODO:!

## Usage

A "subdir" in the REST API is a property in pyncthing. For example,
`GET /rest/cluster/pending/devices` will be done via `sync.cluster.pending.devices()`

```python
from pyncthing import Syncthing

sync = Syncthing("http://localhost:8384/rest")

# This endpoint does not need authentication
assert sync.noauth.health()

# This does NOT check for authentication errors.
sync.set_api_key("<YOUR API KEY RETRIEVED ON THE WEB UI>")

print(sync.system.status())
for name, path in sync.system.paths():
    print(f"System path {name} is {path}")

for folder in sync.config.folders().get():
    print(folder["id"], folder["label"])

# This call is blocking!
# Even next() might block if no event is coming.
# You can stop blocked calls with sync.events.stop().
# Carefull, it blocks *all* calls!
# This API will probably change in the future.
for event in sync.events():
    print(event)

```

## Thank you

* [The Syncthing project](syncthing.net) for an amazing synchronization tool!
* [aiosyncthing](https://github.com/zhulik/aiosyncthing) for a huge inspiration of the coding style of this project.
