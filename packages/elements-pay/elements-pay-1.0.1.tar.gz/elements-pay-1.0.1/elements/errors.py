from __future__ import absolute_import

import json

import requests

from elements import util
from elements.elements_object import ElementsObject


class ErrorObject(ElementsObject):
    @classmethod
    def from_http_body(cls, http_body):
        if http_body is None:
            return None
        try:
            if hasattr(http_body, "decode"):
                http_body = http_body.decode("utf-8")
            json_body = json.loads(http_body)
            if "error" not in json_body or not isinstance(json_body["error"], dict):
                return None
            return util.convert_to_elements_object(json_body["error"])
        except Exception as e:
            util.log_error("Failed parsing request error", body=http_body, error=str(e))
            return None


class ElementsError(Exception):
    """
    Contains the detail error information received from the Elements API,
    refer to https://elements-pay.readme.io/reference/errors for more information.
    """

    def __init__(
        self,
        message=None,
        type=None,
        code=None,
        trace_id=None,
        psp_reference=None,
        param=None,
        decline_code=None,
        http_status=None,
        http_headers=None,
        http_body=None,
        error=None,
    ):
        super(ElementsError, self).__init__(message)
        self.message = message
        self.type = type
        self.code = code
        self.trace_id = trace_id
        self.psp_reference = psp_reference
        self.param = param
        self.decline_code = decline_code
        self.http_status = http_status
        self.http_headers = http_headers
        self.http_body = http_body
        self.error = error


class APIConnectionError(ElementsError):
    def __init__(
        self,
        message=None,
        http_status=None,
        http_headers=None,
        http_body=None,
        cause=None,
    ):
        super(APIConnectionError, self).__init__(
            message,
            http_status=http_status,
            http_headers=http_headers,
            http_body=http_body,
        )
        self.cause = cause

    def retryable(self):
        return isinstance(self.cause, tuple(self._retryable_causes()))

    def _retryable_causes(self):
        return [requests.exceptions.Timeout, requests.exceptions.ConnectionError]


class APIError(ElementsError):
    pass


class InvalidRequestError(ElementsError):
    pass


class IdempotencyError(ElementsError):
    pass


class AuthenticationError(ElementsError):
    pass


class PermissionRequiredError(ElementsError):
    pass


class RateLimitError(ElementsError):
    pass


class CardError(ElementsError):
    pass


class InternalServerError(ElementsError):
    pass


def parse_api_error(http_status, http_headers, http_body):
    error_object = ErrorObject.from_http_body(http_body)
    if error_object is None:
        return APIError(
            message=http_body,
            http_body=http_body,
            http_status=http_status,
            http_headers=http_headers,
        )

    code_to_types = {
        "api_error": APIError,
        "api_connection_error": APIConnectionError,
        "authentication_error": AuthenticationError,
        "invalid_request_error": InvalidRequestError,
        "card_error": CardError,
        "idempotency_error": IdempotencyError,
        "rate_limit_error": RateLimitError,
        "more_permissions_required": PermissionRequiredError,
        "internal_server_error": InternalServerError,
    }
    error_type = code_to_types.get(error_object["type"], APIError)
    error_params = dict(error_object)
    for key in ["http_status", "http_headers", "http_body", "error"]:
        error_params.pop(key, None)

    return error_type(
        http_status=http_status,
        http_headers=http_headers,
        http_body=http_body,
        error=error_object,
        **error_params
    )
