import json
import platform

import requests

import paymob
from paymob.logging import log
from paymob.utils import resource_to_url, api_base_url, next_api_version


class HTTPBaseResource(object):
    """
    HTTP Resource
    """

    RESOURCE_PATH = None

    @classmethod
    def resource_url(cls):
        """
        Resource URL
        """
        if not cls.RESOURCE_PATH:
            raise NotImplementedError(
                "Resource class must have a RESOURCE_PATH string."
            )
        return resource_to_url(cls.RESOURCE_PATH)


class HTTPRequest(object):
    """
    HTTP Requester.
    """

    def __init__(self, method, secret_key=None, resource=None, api_version=None):
        self.secret_key = secret_key or paymob.secret_key
        self.resource = resource
        self.api_version = api_version or next_api_version()
        self.method = method

    @property
    def auth_header(self):
        return "Token {secret_key}".format(secret_key=self.secret_key)

    @property
    def full_url(self):
        url = api_base_url() + self.resource.resource_url()
        return url

    def request(self, payload=None,reference=None, querystr=None):
        url = self.full_url
        # TODO: ADD LOGGER FOR RESPONSE STATUS CODE AND URL PATH INFO
        # TODO: ADD LOGGER FOR RESPONSE BODY DEBUG
        # TODO: ADD LOGGER FOR REQUEST-ID HEADER DEBUG
        log(
            "Sending Request To Paymob, Request URL:\
             {url}, Request Method {method}".format(
                url=url, method=self.method
            ),
            "info",
        )
        # TODO: TRY CATCH
        response = self.pre_request_handler(reference=reference, url=url, payload=payload, querystr=querystr)
        response = self.response_handler(response)
        # TODO: Handle JSON Exceptions
        return response

    def _request_agent_headers(self):
        user_agent = "Paymob Python SDK {version}".format(version=self.api_version)
        user_agent_dict = {
            "sdk_api_version": self.api_version,
            "sdk_language": "python",
            "sdk_authority": "Paymob",
            "sdk_request_client": "name: "
            + str(requests.__title__)
            + " - build: "
            + str(requests.__build__)
            + " - version: "
            + str(requests.__version__),
        }
        for str_value, platform_func in (
            ("sdk_lang_version", platform.python_version),
            ("sdk_platform", platform.platform),
            ("sdk_underlying_sys_info", lambda: " ".join(platform.uname())),
        ):
            try:
                header_value = platform_func()
            except Exception as exception:
                header_value = "UNDEFINED - {exception}".format(exception=exception)
            user_agent_dict[str_value] = header_value
        user_agent_header = {
            "User-Agent": user_agent,
            "X-Paymob-SDK-Agent": json.dumps(user_agent_dict),
        }
        return user_agent_header

    def pre_request_handler(self, url, payload, reference,querystr):
        headers = self.request_headers()
        # TODO: ADD LOGGER FOR URL PATH INFO
        # TODO: ADD LOGGER FOR REQUEST METHOD INFO

        if reference is not None:
            url= url +reference
        if self.method in ["get", "options", "delete"]:
            return getattr(requests, self.method)(url=url, headers=headers, params=querystr)
        return getattr(requests, self.method)(url=url, headers=headers, json=payload)

    def request_headers(self):
        headers = self._request_agent_headers()
        headers["Authorization"] = self.auth_header
        return headers

    def response_handler(self, response):
        response_headers = self._response_header_handler(response)
        # TODO: LOG REQUEST ID
        if "X-Paymob-Request-ID" in response_headers:
            paymob_request_id = response_headers["X-Paymob-Request-ID"]
            log(
                "Paymob Request Trace ID - {paymob_request_id}".format(
                    paymob_request_id=paymob_request_id
                ),
                "debug",
            )
        return response.json()

    def response_error_handler(self):
        pass

    def response_error_mapper(self):
        pass

    def _response_header_handler(self, response):
        headers = response.headers
        return headers
