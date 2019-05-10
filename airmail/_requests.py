import requests

from pytils.classes.meta import StaticMeta
from pytils.paths import AbstractPath

__all__ = [
    'Requests'
]


class Requests(metaclass=StaticMeta):

    @staticmethod
    def get(endpoint: AbstractPath, params=None, **kwargs):
        requests.get(endpoint.path, params, **kwargs)

    @staticmethod
    def post(endpoint: AbstractPath, data=None, **kwargs):
        requests.post(endpoint.path, data, **kwargs)

    @staticmethod
    def put(endpoint: AbstractPath, data=None, **kwargs):
        requests.put(endpoint.path, data, **kwargs)

    @staticmethod
    def delete(endpoint: AbstractPath, **kwargs):
        requests.delete(endpoint.path, **kwargs)

    @staticmethod
    def head(endpoint: AbstractPath, **kwargs):
        requests.head(endpoint.path, **kwargs)

    @staticmethod
    def options(endpoint: AbstractPath, **kwargs):
        requests.options(endpoint.path, **kwargs)
