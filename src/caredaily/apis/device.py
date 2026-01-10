# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///


from .api import API

from ..models import (
    APIKeyType,
)

class Execution(API):
    def listen(
            self,
            app_instance_id: int,
            timeout: int = None,
            clean_time_ms: int = None,
            clean: bool = None,
    ):
        params = {
            "appInstanceId": app_instance_id,
            "timeout": timeout,
            "cleanTime": clean_time_ms,
            "clean": clean,
        }
        params = {k: v for k, v in params.items() if v is not None}
        headers = self.adapter._get_headers()
        if "ADMIN_KEY" in self.adapter._headers:
            headers = self.adapter._get_headers(
                self.adapter._headers.get("ADMIN_KEY"),
                key_type=APIKeyType.USER,
            )
        return self.adapter.get(
            "/deviceio/analytic",
            ep_params=params,
            ep_headers=headers,
        )