from __future__ import absolute_import

from elements.api_resource import APIResource, api_method


@api_method("create", "post", "/api/v1/authentication/client_token")
class ClientToken(APIResource):
    OBJECT_NAME = "client_token"
