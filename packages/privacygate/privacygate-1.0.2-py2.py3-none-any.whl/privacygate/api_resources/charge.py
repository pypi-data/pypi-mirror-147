from privacygate.api_resources.base import CreateAPIResource
from privacygate.api_resources.base import ListAPIResource
from privacygate import util


@util.register_resource_cls
class Charge(ListAPIResource,
             CreateAPIResource):
    RESOURCE_PATH = "charges"
    RESOURCE_NAME = "charge"

    @classmethod
    def cancel(cls, entity_id, **params):
        response = cls._api_client.post(
            cls.RESOURCE_PATH, entity_id, 'cancel',
            data=params
        )
        return util.convert_to_api_object(response, cls._api_client, cls)

    @classmethod
    def resolve(cls, entity_id, **params):
        response = cls._api_client.post(
            cls.RESOURCE_PATH, entity_id, 'resolve',
            data=params
        )
        return util.convert_to_api_object(response, cls._api_client, cls)
