from privacygate.api_resources.base import CreateAPIResource
from privacygate.api_resources.base import DeleteAPIResource
from privacygate.api_resources.base import ListAPIResource
from privacygate.api_resources.base import UpdateAPIResource
from privacygate.util import register_resource_cls


@register_resource_cls
class Checkout(ListAPIResource,
               CreateAPIResource,
               UpdateAPIResource,
               DeleteAPIResource):
    RESOURCE_PATH = "checkouts"
    RESOURCE_NAME = "checkout"
