from __future__ import absolute_import

from elements.api_resource import APIResource, api_method


@api_method("delete", "delete", "/api/v1/customers/{external_customer_id}")
class Customer(APIResource):
    OBJECT_NAME = "customer"
