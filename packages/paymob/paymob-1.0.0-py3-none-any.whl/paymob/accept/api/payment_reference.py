from paymob.http import HTTPBaseResource
from paymob.http_mixins import CreateResourceMixin

class Refund(CreateResourceMixin, HTTPBaseResource):
    RESOURCE_PATH= "payment-reference/refund"

class Void(CreateResourceMixin,HTTPBaseResource):
    RESOURCE_PATH= "payment-reference/void"

class Capture(CreateResourceMixin,HTTPBaseResource):
    RESOURCE_PATH= "payment-reference/capture"
