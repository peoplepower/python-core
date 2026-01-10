# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
#   "pydantic",
# ]
# ///

import logging
from json import JSONDecodeError
from typing import Dict

import requests
import requests.packages

from .exceptions import CareDailyException
from .models import (
    APIKeyType,
    Result,
    ResultCode,
)


class RestAdapter:
    """
    RestAdapter is a class that provides a simple interface to make HTTP requests to a REST API.
    """

    def __init__(
        self,
        hostname: str = "app.peoplepowerco.com",
        api_key: str = None,
        key_type: APIKeyType = None,
        ssl_verify: bool = True,
        proxies: Dict = None,
        logger: logging.Logger = None,
    ):
        """
        Constructor for RestAdapter.
        :param hostname: The hostname of the API.
        :param api_key: The API key to use for requests.
        :param key_type: The type of key to use for requests.
        :param ssl_verify: Whether to verify SSL certificates.
        :param logger: The logger to use for logging.
        """
        self.url = f"https://{hostname}"
        try:
            key_type = key_type if isinstance(key_type, APIKeyType) else APIKeyType(int(f"{key_type}"))
        except ValueError:
            key_type = None
        self._headers = self._get_headers(api_key, key_type)
        self._ssl_verify = ssl_verify
        if not ssl_verify:
            # noinspection PyUnresolvedReferences
            requests.packages.urllib3.disable_warnings()
        self._proxies = proxies
        self._logger = logger or logging.getLogger(__name__)
        self._logger.debug(f"RestAdapter: url={self.url} headers={self._headers}")

    def _get_headers(self, api_key: str = None, key_type: APIKeyType = None) -> Dict:
        """
        Get the headers to use for requests.
        :param api_key: The API key to use for requests.
        :param key_type: The type of key to use for requests.
        :return: The headers to use for requests.
        """
        headers = {
            "Content-Type": "application/json",
        }
        if key_type is None:
            return headers
        if key_type == APIKeyType.USER:
            headers.update({"API_KEY": api_key})
        if key_type == APIKeyType.ADMIN:
            headers.update({"ADMIN_KEY": api_key})
        if key_type == APIKeyType.ANALYTIC:
            headers.update({"ANALYTIC_API_KEY": api_key})
        return headers

    def _do(
        self,
        http_method: str,
        endpoint: str,
        ep_headers: Dict = None,
        ep_params: Dict = None,
        ep_json: Dict = None,
        ep_data = None,
    ):
        """
        Perform an HTTP request.
        :param http_method: The HTTP method to use.
        :param endpoint: The endpoint to request.
        :param ep_headers: The headers to use for the request.
        :param ep_params: The parameters to use for the request.
        :param ep_json: The JSON data to use for the request.
        :param ep_data: The data to use for the request.
        :return: The result of the request.
        """
        full_url = self.url + endpoint
        headers = {**self._headers, **ep_headers} if ep_headers else self._headers
        log_line_pre = f"method={http_method} url={full_url} headers={headers} params={ep_params} json={ep_json} data={ep_data}"
        log_line_post = "success={} result_code={} message={}"
        try:
            self._logger.debug(msg=log_line_pre)
            response = requests.request(
                method=http_method,
                url=full_url,
                verify=self._ssl_verify,
                headers=headers,
                params=ep_params,
                json=ep_json,
                data=ep_data,
                proxies=self._proxies,
            )
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise CareDailyException("Request failed") from e
        is_success = response.status_code >= 200 and response.status_code <= 299
        content_type = response.headers.get("Content-Type", headers.get("Content-Type"))
        self._logger.debug(f"response={response.text}")
        if "application/json" in content_type:
            try:
                data_out = response.json()
            except (ValueError, JSONDecodeError) as e:
                self._logger.error(
                    msg=log_line_pre + log_line_post.format(False, -1, e)
                )
                raise CareDailyException("Bad JSON response") from e

            log_line = log_line_pre + log_line_post.format(
                is_success,
                data_out.get("resultCode", -1),
                data_out.get("resultCodeMessage"),
            )
            if is_success:
                try:
                    self._logger.debug(msg=log_line)
                    result = Result.model_validate(data_out)
                except Exception as e:
                    self._logger.error(
                        msg=log_line_pre
                        + log_line_post.format(True, data_out.get("resultCode", -1), e)
                    )
                    raise CareDailyException("Invalid JSON") from e
                if (
                    result.result_code is not None
                    and result.result_code != ResultCode.SUCCESS
                ):
                    raise CareDailyException(
                        message=f"[{result.result_code.value}] {result.result_code_message}",
                        context=data_out,
                    )
                result.data = data_out
                return result
            self._logger.error(msg=log_line)
            raise Exception(data_out["message"])
        if "text/" in content_type:
            log_line = log_line_pre + log_line_post.format(
                is_success,
                response.status_code,
                response.text,
            )
            if is_success:
                self._logger.debug(msg=log_line)
                return Result(
                    **{
                        "resultCode": 0,
                        "data": {"text": response.text},
                    }
                )
            self._logger.error(msg=log_line)
            raise CareDailyException(response.text)
        if "application/xml" in content_type:
            log_line = log_line_pre + log_line_post.format(
                is_success,
                response.status_code,
                response.text,
            )
            if is_success:
                self._logger.debug(msg=log_line)
                return Result(
                    **{
                        "resultCode": 0,
                        "data": {"text": response.text},
                    }
                )
            self._logger.error(msg=log_line)
            raise CareDailyException(response.text)
        self._logger.error(
            msg=log_line_pre + log_line_post.format(False, -1, "Bad response")
        )
        raise CareDailyException("Bad response")

    def get(
        self,
        endpoint: str,
        ep_headers: Dict = None,
        ep_params: Dict = None,
        ep_json: Dict = None,
        ep_data = None,
    ) -> Result:
        """
        Perform a GET request.
        :param endpoint: The endpoint to request.
        :param ep_headers: The headers to use for the request.
        :param ep_params: The parameters to use for the request.
        :param ep_json: The JSON data to use for the request.
        :param ep_data: The data to use for the request.
        :return: The result of the request.
        """
        return self._do(
            http_method="GET",
            endpoint=endpoint,
            ep_headers=ep_headers,
            ep_params=ep_params,
            ep_json=ep_json,
            ep_data=ep_data
        )

    def post(
        self,
        endpoint: str,
        ep_headers: Dict = None,
        ep_params: Dict = None,
        ep_json: Dict = None,
        ep_data = None,
    ) -> Result:
        """
        Perform a POST request.
        :param endpoint: The endpoint to request.
        :param ep_headers: The headers to use for the request.
        :param ep_params: The parameters to use for the request.
        :param ep_json: The JSON data to use for the request.
        :param ep_data: The data to use for the request.
        :return: The result of the request.
        """
        return self._do(
            http_method="POST",
            endpoint=endpoint,
            ep_headers=ep_headers,
            ep_params=ep_params,
            ep_json=ep_json,
            ep_data=ep_data
        )

    def put(
        self,
        endpoint: str,
        ep_headers: Dict = None,
        ep_params: Dict = None,
        ep_json: Dict = None,
        ep_data = None,
    ) -> Result:
        """
        Perform a PUT request.
        :param endpoint: The endpoint to request.
        :param ep_headers: The headers to use for the request.
        :param ep_params: The parameters to use for the request.
        :param ep_json: The JSON data to use for the request.
        :param ep_data: The data to use for the request.
        :return: The result of the request.
        """
        return self._do(
            http_method="PUT",
            endpoint=endpoint,
            ep_headers=ep_headers,
            ep_params=ep_params,
            ep_json=ep_json,
            ep_data=ep_data
        )

    def delete(
        self,
        endpoint: str,
        ep_headers: Dict = None,
        ep_params: Dict = None,
        ep_json: Dict = None,
        ep_data = None,
    ) -> Result:
        """
        Perform a DELETE request.
        :param endpoint: The endpoint to request.
        :param ep_headers: The headers to use for the request.
        :param ep_params: The parameters to use for the request.
        :param ep_json: The JSON data to use for the request.
        :param ep_data: The data to use for the request.
        :return: The result of the request.
        """
        return self._do(
            http_method="DELETE",
            endpoint=endpoint,
            ep_headers=ep_headers,
            ep_params=ep_params,
            ep_json=ep_json,
            ep_data=ep_data,
        )
