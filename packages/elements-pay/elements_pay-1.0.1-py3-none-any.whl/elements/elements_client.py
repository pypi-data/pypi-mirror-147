from __future__ import absolute_import

import threading
import json
import random
import time

import requests

from elements import util
from elements import errors
from elements import six


class ElementsClient(object):
    """
    Executes HTTP requests against the Elements API,
    converts the response into a resource object or an error object accordingly.
    """

    def __init__(self):
        self._thread_local = threading.local()
        self._thread_local.session = requests.Session()

    def request(self, method, path, params=None, headers=None):
        from elements import ssl_verify_certs, ssl_ca_file

        kwargs = {}
        if ssl_verify_certs:
            kwargs["verify"] = ssl_ca_file
        else:
            kwargs["verify"] = False

        if method.lower() in ["get", "head", "delete"]:
            post_data = None
            query = params
        else:
            post_data = params
            query = None

        post_data = self._encode_post_data(post_data)
        query = self._encode_query(query)
        url = self._full_url(path, query)

        try:
            result = self._thread_local.session.request(
                method, url, headers=headers, data=post_data, **kwargs
            )
        except Exception as e:
            raise self._wrap_requests_exception(e)

        return result.status_code, result.content, result.headers

    def _wrap_requests_exception(self, exception):
        if isinstance(exception, requests.exceptions.SSLError):
            message = "Failed to verify SSL certificate"
        elif isinstance(
            exception,
            (requests.exceptions.Timeout, requests.exceptions.ConnectionError),
        ):
            message = "Unexpected connection error"
        else:
            message = "Unexpected error"
        return errors.APIConnectionError(message, cause=exception)

    def request_with_retries(self, method, path, params=None, headers=None):
        num_retries = 0

        while True:
            response, error = None, None
            try:
                response = self.request(method, path, params, headers)
            except Exception as e:
                error = e

            if self._should_retry(response, error, num_retries):
                util.log_info("Retryable error", error=repr(error))
                num_retries += 1
                sleep_duration = self._sleep_duration(num_retries)
                util.log_info(
                    "Retrying network request",
                    retries=num_retries,
                    sleep_duration=sleep_duration,
                    method=method,
                    path=path,
                )
                time.sleep(sleep_duration)
            else:
                if response is not None:
                    # this response might still be error, but it is certainly non-retryable error
                    return response

                util.log_error("Non-retryable error", error=repr(error))
                raise error

    def _encode_post_data(self, post_data):
        if post_data:
            return json.dumps(post_data, sort_keys=True)
        return None

    def _encode_query(self, query):
        if query:
            return "&".join(
                ["%s=%s" % (k, v) for (k, v) in sorted(six.iteritems(query))]
            )
        return None

    def _full_url(self, path, query):
        if query:
            return path + "?" + query
        return path

    def _sleep_duration(self, num_retries):
        from elements import min_network_retry_delay, max_network_retry_delay

        duration = min_network_retry_delay * (2 ** (num_retries - 1))
        # adding jitter, https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/
        duration = random.uniform(0, 1) * duration
        duration = max(min_network_retry_delay, duration)
        duration = min(max_network_retry_delay, duration)
        return duration

    def _should_retry(self, response, exception, num_retries):
        from elements import max_network_retries

        if num_retries >= max_network_retries:
            return False

        if response is None:
            return (
                isinstance(exception, errors.APIConnectionError)
                and exception.retryable()
            )

        status_code, content, headers = response
        if status_code in [409, 503]:  # retry on conflict or service unavailable
            return True

        return False


default_client = ElementsClient()
