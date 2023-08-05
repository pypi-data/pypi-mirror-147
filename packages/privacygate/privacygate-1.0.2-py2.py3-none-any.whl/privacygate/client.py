import textwrap

import requests

from privacygate.api_resources.charge import Charge
from privacygate.api_resources.checkout import Checkout
from privacygate.api_resources.event import Event
from privacygate.auth import APIAuth
from privacygate.compat import quote
from privacygate.compat import urljoin
from privacygate.error import APIError
from privacygate.error import build_api_error
from privacygate.response import PrivacyGateResponse
from privacygate.util import check_uri_security, lazy_property
from privacygate.util import encode_params


class Client(object):
    """
    API Client for the PrivacyGate API.
    Entry point for making requests to the PrivacyGate API.
    Full API docs available here: https://privacygate.io/docs
    """
    BASE_API_URI = 'https://api.privacygate.io/'
    API_VERSION = '2018-03-22'

    def __init__(self, api_key, base_api_uri=None, api_version=None, timeout=None):
        # Allow passing in a different API base and API version.
        self.BASE_API_URI = check_uri_security(base_api_uri or self.BASE_API_URI)
        self.API_VERSION = api_version or self.API_VERSION
        # Set up a requests session for interacting with the API.
        self.session = self._build_session(APIAuth, api_key, self.API_VERSION)
        # Set up request timeout. None means no timeout.
        self.timeout = timeout

    # Set api resource relations. with lazy evaluated descriptors
    # ---->
    @lazy_property
    def charge(self):
        setattr(Charge, '_api_client', self)
        return Charge

    @lazy_property
    def checkout(self):
        setattr(Checkout, '_api_client', self)
        return Checkout

    @lazy_property
    def event(self):
        setattr(Event, '_api_client', self)
        return Event
    # <----

    def _create_api_uri(self, *parts):
        return urljoin(self.BASE_API_URI, '/'.join(map(quote, parts)))

    def _build_session(self, auth_class, *args, **kwargs):
        session = requests.session()
        session.auth = auth_class(*args, **kwargs)
        session.headers.update({'Accept': 'application/json',
                                'Content-Type': 'application/json'})
        return session

    def _request(self, method, *relative_path_parts, **kwargs):
        """
        Internal helper for creating HTTP requests to the PrivacyGate API.
        Raises the appropriate exceptions when necessary; otherwise, returns the
        response.
        """
        uri = self._create_api_uri(*relative_path_parts)
        data = kwargs.pop('data', None)

        if data and isinstance(data, dict):
            kwargs['data'] = encode_params(data)

        if self.timeout:
            kwargs['timeout'] = self.timeout

        try:
            response = getattr(self.session, method)(uri, **kwargs)
        except Exception as e:
            self._handle_request_error(e)
        else:
            proceeded_response = self._proceed_response(response)
            return proceeded_response

    def _proceed_response(self, response):
        if not response.ok:
            raise build_api_error(response)
        return PrivacyGateResponse(body=response.content,
                                code=response.status_code,
                                headers=response.headers)

    def _handle_request_error(self, e):
        if isinstance(e, requests.exceptions.RequestException):
            msg = "Unexpected error communicating with PrivacyGate."
            err = "{}: {}".format(type(e).__name__, str(e))
        else:
            msg = ("Unexpected error communicating with PrivacyGate. "
                   "It looks like there's probably a configuration "
                   "issue locally.")
            err = "A {} was raised".format(type(e).__name__)
            if str(e):
                err += " with error message {}".format(str(e))
            else:
                err += " with no error message"
        msg = textwrap.fill(msg) + "\n\n(Network error: {})".format(err)
        raise APIError(msg)

    def get(self, *args, **kwargs):
        return self._request('get', *args, **kwargs)

    def post(self, *args, **kwargs):
        return self._request('post', *args, **kwargs)

    def put(self, *args, **kwargs):
        return self._request('put', *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self._request('delete', *args, **kwargs)

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
