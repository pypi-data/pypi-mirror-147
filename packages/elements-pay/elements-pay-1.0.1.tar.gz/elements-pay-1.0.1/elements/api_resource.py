from __future__ import absolute_import

import uuid
from string import Formatter

import elements
from elements import elements_client
from elements.elements_object import ElementsObject
from elements.elements_response import ElementsResponse
from elements import errors
from elements import util


def api_method(name, method, path):
    if method not in ["get", "post", "delete"]:
        raise ValueError(
            "Invalid method: {method}, must be one of "
            "'get', 'post', or 'delete'".format(method=method)
        )

    def wrapper(cls):

        path_param_names = [
            param for _, param, _, _ in Formatter().parse(path) if param is not None
        ]

        if "id" in path_param_names:

            def api_method_request(cls, id, **params):
                path_params = to_path_params(params, path_param_names)

                if "id" in path_param_names:
                    if id is None:
                        raise ValueError("Must provide resource id")
                    path_params["id"] = id

                return cls.execute_resource_request(
                    method, path.format(**path_params), **params
                )

            setattr(cls, name, classmethod(api_method_request))
            return cls
        else:

            def api_method_request(cls, **params):
                path_params = to_path_params(params, path_param_names)

                return cls.execute_resource_request(
                    method, path.format(**path_params), **params
                )

            setattr(cls, name, classmethod(api_method_request))
            return cls

    return wrapper


def to_path_params(params, path_param_names):
    return dict(
        [(param_name, params.pop(param_name, None)) for param_name in path_param_names]
    )


def _full_path(path, api_base=None):
    api_base = api_base or elements.api_base
    return "{api_base}{path}".format(api_base=api_base, path=path)


def _request_headers(method, api_key=None, idempotency_key=None):
    api_key = api_key or elements.api_key
    headers = dict()
    headers["Authorization"] = "Bearer {api_key}".format(api_key=api_key)
    headers["Content-Type"] = "application/json"
    if method.lower() in ["post", "delete"]:
        headers["Idempotency-Key"] = idempotency_key or str(uuid.uuid4())
    headers["User-Agent"] = "elements-python-sdk/{version}".format(
        version=elements.version
    )
    return headers


class APIResource(ElementsObject):
    """
    All API resources, such as Charges, Refunds, extends from this class.

    Each API resource should have an OBJECT_NAME, corresponding to the "type" in a JSON response of that resource.

    API endpoints are defined with a special decorator `api_method`:

    @api_method("create", "post", "/api/v1/charges")
    class Charge(APIResource):
        OBJECT_NAME = "charge"

    To break it down, the decorator accepts three arguments
    1. name of the api method, e.g., "create", this also becomes the name of the class method to invoke this api request
    2. the http verb of this API request, e.g., "post"
    3. the path of this API request, e.g., "/api/v1/charges"

    To invoke this API method:

    charge = elements.Charge.create(
        amount=300000,
        currency="USD",
        payment_method_token="token"
    )

    Here, the class method accepts kwargs for constructing request params.
    Note that if the API path consists any path parameters,
    e.g., charge_id in /api/v1/charges/{id}/capture, then it will also be
    looked up from the supplied kwargs when the request is being made.

    There are a couple of special params: api_base, api_key, and idempotency_key.
    api_base and api_key are used to override default configuration, whereas
    idempotency_key will be sent in the headers.
    """

    @classmethod
    def execute_resource_request(cls, method, path, **params):
        client = elements_client.default_client
        api_base = params.pop("api_base", None)
        api_key = params.pop("api_key", None)
        idempotency_key = params.pop("idempotency_key", None)
        headers = _request_headers(method, api_key, idempotency_key)
        path = _full_path(path, api_base)

        logging_context = dict(
            method=method, path=path, idempotency_key=idempotency_key
        )

        cls._log_request(logging_context, params, headers)

        code, body, headers = client.request_with_retries(method, path, params, headers)

        cls._log_response(logging_context, code, body, headers)

        resp = cls.handle_response(code, body, headers, logging_context)

        return util.convert_to_elements_object(resp.data)

    @classmethod
    def _log_request(cls, context, params=None, headers=None):
        util.log_info(
            "API request",
            method=context["method"],
            path=context["path"],
            idempotency_key=context["idempotency_key"],
        )
        util.log_debug("API request details", params=params, headers=headers)

    @classmethod
    def _log_response(cls, context, code=None, body=None, headers=None):
        util.log_info(
            "API response",
            method=context["method"],
            path=context["path"],
            idempotency_key=context["idempotency_key"],
            code=code,
        )
        util.log_debug("API response details", body=body, headers=headers)

    @classmethod
    def handle_response(cls, code, body, headers, context):
        if code >= 400:
            error = errors.parse_api_error(
                http_status=code, http_headers=headers, http_body=body
            )
            util.log_error(
                "API request error, error: %s" % error.message,
                method=context["method"],
                path=context["path"],
                code=code,
                idempotency_key=context["idempotency_key"],
            )
            raise error

        try:
            if hasattr(body, "decode"):
                body = body.decode("utf-8")
            return ElementsResponse(code, body, headers)
        except Exception as e:
            util.log_error(
                "Malformed API response",
                method=context["method"],
                path=context["path"],
                code=code,
                idempotency_key=context["idempotency_key"],
            )
            raise errors.APIError(
                "Received malformed response body, error: %s" % str(e),
                code,
                headers,
                body,
            )
