from __future__ import absolute_import

from elements.api_resource import APIResource, api_method


@api_method("create", "post", "/api/v1/checkout/sessions")
@api_method("retrieve", "get", "/api/v1/checkout/sessions/{id}")
@api_method("list", "get", "/api/v1/checkout/sessions")
class CheckoutSession(APIResource):
    OBJECT_NAME = "checkout_session"
