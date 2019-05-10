import collections.abc
from typing import Any, ByteString, ItemsView, Iterable, Iterator, KeysView, Mapping, Sequence, Text, ValuesView

__all__ = [
    'ObjectView',
]


class ObjectView(collections.abc.Sequence, collections.abc.Mapping):

    def __init__(self, data: Any):
        object.__setattr__(self, '_ov_backing_data', data)

    __slots__ = ('_ov_backing_data',)

    @staticmethod
    def _select_view_ctor(data: Any):
        if isinstance(data, (Mapping, Sequence)) \
                and not isinstance(data, (Text, ByteString)):
            return ObjectView
        else:
            return lambda x: x

    @classmethod
    def _ov_wrap(cls, data: Any) -> Any:
        return cls._select_view_ctor(data)(data)

    @staticmethod
    def _ov_unwrap(view: Any) -> Any:
        return view() if isinstance(view, ObjectView) else view

    @classmethod
    def of(cls, data: Any) -> Any:
        return cls._ov_wrap(data)

    @staticmethod
    def get_value(view: Any) -> Any:
        return ObjectView._ov_unwrap(view)

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self._ov_backing_data!r})'

    def __str__(self) -> str:
        return str(self._ov_backing_data)

    def __bytes__(self):
        return bytes(self._ov_backing_data)

    def __format__(self, format_spec: str) -> str:
        return format(self._ov_backing_data, format_spec)

    def __hash__(self):
        return hash(self._ov_backing_data)

    def __bool__(self):
        return bool(self._ov_backing_data)

    def __getattr__(self, key: str):
        return self._ov_wrap(self._ov_backing_data[key])

    def __setattr__(self, key: str, value):
        self._ov_backing_data[key] = value

    def __delattr__(self, key: str):
        del self._ov_backing_data[key]

    def __call__(self):
        return self._ov_backing_data

    def __len__(self):
        return len(self._ov_backing_data)

    def __getitem__(self, key):
        return self._ov_wrap(self._ov_backing_data[key])

    def __setitem__(self, key, value):
        self._ov_backing_data[key] = value

    def __delitem__(self, key):
        del self._ov_backing_data[key]

    def _ov_wrap_iterable(self, iterable: Iterable) -> Iterator:
        return (self._ov_wrap(item) for item in iterable)

    def __iter__(self):
        return self._ov_wrap_iterable(iter(self._ov_backing_data))

    def __reversed__(self):
        return self._ov_wrap_iterable(reversed(self._ov_backing_data))

    def __contains__(self, item):
        return item in self._ov_backing_data

    def keys(self) -> KeysView:
        return self._ov_backing_data.keys()

    def values(self) -> ValuesView:
        return ObjectView.Values(self)

    def items(self) -> ItemsView:
        return ObjectView.Items(self)

    def _values(self) -> Iterator:
        return self._ov_wrap_iterable(self._ov_backing_data.values())

    def _items(self) -> Iterator:
        return (
            (key, self._ov_wrap(value))
            for key, value in self._ov_backing_data.items()
        )

    class Values(collections.abc.ValuesView):

        def __init__(self, data: 'ObjectView'):
            super().__init__(data)
            self._data = data

        def __iter__(self) -> Iterator:
            return self._data._values()

    class Items(collections.abc.ItemsView):

        def __init__(self, data: 'ObjectView'):
            super().__init__(data)
            self._data = data

        def __iter__(self) -> Iterator:
            return self._data._items()
