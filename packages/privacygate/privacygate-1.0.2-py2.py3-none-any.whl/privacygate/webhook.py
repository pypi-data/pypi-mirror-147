import hmac
import json
from hashlib import sha256

from privacygate.api_resources import Event
from privacygate.error import SignatureVerificationError
from privacygate.error import WebhookInvalidPayload
from privacygate.util import secure_compare


class Webhook(object):
    """
    Analyze and construct appropriate event object based on webhook notification
    """

    @staticmethod
    def construct_event(payload, sig_header, secret):
        try:
            data = json.loads(payload)
        except ValueError:
            raise WebhookInvalidPayload('Invalid payload provided. '
                                        'No JSON object could be decoded')
        event = data.get('event')
        if not event:
            raise WebhookInvalidPayload('Invalid payload provided')
        WebhookSignature.verify_sig_header(payload, sig_header, secret)
        return Event(data=event)


class WebhookSignature(object):

    @staticmethod
    def _compute_signature(payload, secret):
        mac = hmac.new(secret.encode('utf-8'),
                       msg=payload.encode('utf-8'),
                       digestmod=sha256)
        return mac.hexdigest()

    @classmethod
    def verify_sig_header(cls, payload, sig_header, secret):
        comptuted_sig = cls._compute_signature(payload, secret)
        if not secure_compare(comptuted_sig, sig_header):
            raise SignatureVerificationError(sig_header, payload)
        return True
