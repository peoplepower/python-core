# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///

from typing import Dict

from ..http import RestAdapter


class API:
    def __init__(self, config: Dict = {}):
        kwargs = {
            "hostname": config.get("hostname"),
            "api_key": config.get("api_key"),
            "key_type": config.get("key_type"),
            "ssl_verify": config.get("ssl_verify", True),
            "proxies": config.get("proxies"),
            "logger": config.get("logger"),
        }
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        self.adapter = RestAdapter(**kwargs)