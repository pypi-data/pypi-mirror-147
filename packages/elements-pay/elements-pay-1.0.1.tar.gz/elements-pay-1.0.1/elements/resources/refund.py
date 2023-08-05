from __future__ import absolute_import

from elements.api_resource import APIResource, api_method


@api_method("create", "post", "/api/v1/refunds")
@api_method("retrieve", "get", "/api/v1/refunds/{id}")
@api_method("list", "get", "/api/v1/refunds")
class Refund(APIResource):
    OBJECT_NAME = "refund"
