import datetime
import sys
import json


class LazyLoader(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        object.__setattr__(self, 'id', kwargs['id'])
        object.__setattr__(self, '_loaded', False)

    def __sizeof__(self):
        return super().__sizeof__() + sys.getsizeof(self.id) + sys.getsizeof(self._loaded)

    def _remove(self):
        del self.id
        del self._loaded
        return super()._remove()

    def __getattribute__(self, item):
        if item is 'id':
            return object.__getattribute__(self, 'id')
        if not object.__getattribute__(self, '_loaded'):
            object.__getattribute__(self, '_load')()
        return super().__getattribute__(item)

    def __setattr__(self, key, value):
        object.__getattribute__(self, '_store')(key, value)
        return super().__setattr__(key, value)

    def __setitem__(self, key, value):
        object.__getattribute__(self, '_store')(key, value)
        return super().__setitem__(key, value)

    def __getitem__(self, item):
        if not object.__getattribute__(self, '_loaded'):
            object.__getattribute__(self, '_load')()
        return super().__getitem__(item)

    def _load(self):
        if object.__getattribute__(self, 'id') is None:
            raise IndexError('The ID is not set')
        pass  # TODO implement this. Load source and destination
        object.__setattr__(self, '_loaded', True)

    def _store(self, key, value):
        pass

    def _unload(self):
        pass


class LastAccessed(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        object.__getattribute__(self, '_set_last_accessed')()

    def _get_current_time(self):
        return datetime.datetime.now()

    def _set_last_accessed(self):
        return object.__setattr__(self, '_last_accessed', object.__getattribute__(self, '_get_current_time')())

    def __sizeof__(self):
        return super().__sizeof__() + sys.getsizeof(self._last_accessed)

    def _remove(self):
        del self._last_accessed
        return super()._remove()

    def __getattribute__(self, item):
        if item not in ('_last_accessed', '_loaded'):
            object.__getattribute__(self, '_set_last_accessed')()
        return super().__getattribute__(item)

    def __setitem__(self, key, value):
        object.__getattribute__(self, '_set_last_accessed')()
        return super().__setitem__(key, value)

    def __getitem__(self, item):
        object.__getattribute__(self, '_set_last_accessed')()
        return super().__getitem__(item)

    def _e_dec(func):
        def inner(self, rhs):
            self._set_last_accessed()
            try:
                rhs._set_last_accessed()
            except AttributeError:
                pass
            return func(self, rhs)
        return inner

    @_e_dec
    def __eq__(self, other):
        return other is self

    def _e(op):
        def func(self, rhs):
            object.__getattribute__(self, '_set_last_accessed')()
            if isinstance(rhs, LastAccessed):
                object.__getattribute__(rhs, '_set_last_accessed')()
            return getattr(super(), '{}'.format(op))(rhs)
        return func

    __lt__ = _e('__lt__')
    __le__ = _e('__le__')
    __gt__ = _e('__gt__')
    __ge__ = _e('__ge__')
    __ne__ = _e('__ne__')

    __add__ = _e('__add__')
    __sub__ = _e('__sub__')
    __mul__ = _e('__mul__')
    __truediv__ = _e('__truediv__')
    __floordiv__ = _e('__floordiv__')
    __mod__ = _e('__mod__')
    __divmod__ = _e('__divmod__')
    __pow__ = _e('__pow__')
    __lshift__ = _e('__lshift__')
    __rshift__ = _e('__rshift__')
    __and__ = _e('__and__')
    __xor__ = _e('__xor__')
    __or__ = _e('__or__')


class Node(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        object.__setattr__(self, 'id', kwargs['id'])

    def __hash__(self):
        return object.__getattribute__(self, 'id')

    def __setattr__(self, key, value):
        return self.__setitem__(key, value)

    def __getattr__(self, item):
        return self.__getitem__(item)


class LiteNode(Node):
    """A lite version of the node"""
    def __init__(self, id=None, *args, **kwargs):
        super().__init__(id=id, *args, **kwargs)
        object.__setattr__(self, 'sources', set())
        object.__setattr__(self, 'destinations', set())


class LazyLoadNode(LazyLoader, LastAccessed, Node):
    def __init__(self, id=None, *args, **kwargs):
        super().__init__(id=id, *args, **kwargs)
        object.__setattr__(self, 'sources', set())
        object.__setattr__(self, 'destinations', set())

    def __sizeof__(self):
        return super().__sizeof__() + (sys.getsizeof(object.__getattribute__(self, 'sources')) +
                                       sys.getsizeof(object.__getattribute__(self, 'destinations')))

    def _remove(self):
        del self.sources
        del self.destinations
        super()._remove()
        del self


class LiteRelation(Node):
    def __init__(self, source=None, label=None, destination=None, id=None, *args, **kwargs):
        super().__init__(id=id, *args, **kwargs)
        object.__setattr__(self, 'source', source)
        object.__setattr__(self, 'destination', destination)
        object.__setattr__(self, 'label', label)

    def __repr__(self):
        return object.__getattribute__(self, 'label')


class LazyLoadRelation(Node, LazyLoader, LastAccessed):
    def __init__(self, source=None, label=None, destination=None, id=None, *args, **kwargs):
        super().__init__(id=id, *args, **kwargs)
        object.__setattr__(self, 'source', source)
        object.__setattr__(self, 'destination', destination)
        object.__setattr__(self, 'label', label)

    def __sizeof__(self):
        return super().__sizeof__() + (sys.getsizeof(self.source) + sys.getsizeof(self.destination) +
                                        sys.getsizeof(self.label))

    def _remove(self):
        del self.source
        del self.destination
        del self.label
        super()._remove()
        del self

    def __repr__(self):
        return object.__getattribute__(self, 'label')
