from __future__ import absolute_import

from elements.api_resource import APIResource, api_method


@api_method("retrieve", "get", "/api/v1/payment_methods/{id}")
@api_method("create", "post", "/api/v1/payment_methods")
class PaymentMethod(APIResource):
    OBJECT_NAME = "customer_payment_method"
