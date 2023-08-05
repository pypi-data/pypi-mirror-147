from __future__ import absolute_import

from elements.api_resource import APIResource, api_method


@api_method("retrieve", "get", "/api/v1/tokens/retrieve")
class Token(APIResource):
    OBJECT_NAME = "token"
