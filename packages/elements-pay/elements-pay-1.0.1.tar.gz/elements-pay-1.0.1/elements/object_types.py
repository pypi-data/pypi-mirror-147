from __future__ import absolute_import

from elements import resources

OBJECT_TYPES = {
    resources.Charge.OBJECT_NAME: resources.Charge,
    resources.ClientToken.OBJECT_NAME: resources.ClientToken,
    resources.Dispute.OBJECT_NAME: resources.Dispute,
    resources.Refund.OBJECT_NAME: resources.Refund,
    resources.PaymentMethod.OBJECT_NAME: resources.PaymentMethod,
    resources.PaymentMethodGateway.OBJECT_NAME: resources.PaymentMethodGateway,
    resources.Token.OBJECT_NAME: resources.Token,
    resources.CheckoutSession.OBJECT_NAME: resources.CheckoutSession,
    resources.Customer.OBJECT_NAME: resources.Customer,
}
