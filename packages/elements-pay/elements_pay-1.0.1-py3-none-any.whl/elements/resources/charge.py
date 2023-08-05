from __future__ import absolute_import

from elements.api_resource import APIResource, api_method


@api_method("create", "post", "/api/v1/charges")
@api_method("capture", "post", "/api/v1/charges/{id}/capture")
@api_method("cancel", "post", "/api/v1/charges/{id}/cancel")
@api_method("retrieve", "get", "/api/v1/charges/{id}")
@api_method("list", "get", "/api/v1/charges")
class Charge(APIResource):
    OBJECT_NAME = "charge"
