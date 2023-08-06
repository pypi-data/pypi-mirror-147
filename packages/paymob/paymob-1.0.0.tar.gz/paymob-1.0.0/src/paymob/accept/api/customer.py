from paymob.http import HTTPBaseResource
from paymob.http_mixins import CreateResourceMixin, RetrieveResourceMixin, ListResourceMixin


class Customer(CreateResourceMixin, RetrieveResourceMixin, ListResourceMixin, HTTPBaseResource):
    RESOURCE_PATH = "customer"


