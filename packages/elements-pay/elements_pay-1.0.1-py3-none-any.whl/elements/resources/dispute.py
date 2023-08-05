from __future__ import absolute_import

from elements.api_resource import APIResource, api_method


@api_method("retrieve", "get", "/api/v1/disputes/{dispute_id}")
@api_method("list", "get", "/api/v1/disputes")
class Dispute(APIResource):
    OBJECT_NAME = "dispute"
