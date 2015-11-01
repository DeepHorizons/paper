import datetime
import itertools


class Base(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_last_accessed()

    def _get_current_time(self):
        return datetime.datetime.now()

    def _set_last_accessed(self):
        self.set_attr('_last_accessed', self._get_current_time())

    def set_attr(self, key, value):
        """Access to the set attr method since we overwrite it"""
        super().__setattr__(key, value)

    def __hash__(self):
        self._set_last_accessed()
        return self.id

    def __setattr__(self, key, value):
        # No need to set accessed here, is set in __setitem__
        return self.__setitem__(key, value)

    def __getattr__(self, item):
        # No need to set accessed here, is set in __getitem__
        return self.__getitem__(item)

    def __getattribute__(self, item):
        if item != '_last_accessed':
            super().__setattr__('_last_accessed', datetime.datetime.now())
        return super().__getattribute__(item)

    def __setitem__(self, key, value):
        self._set_last_accessed()
        return super().__setitem__(key, value)

    def __getitem__(self, item):
        self._set_last_accessed()
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
            self._set_last_accessed()
            try:
                rhs._set_last_acessed()
            except AttributeError:
                pass
            if '__' in op:
                return getattr(super(), '{}'.format(op))(rhs)
            return getattr(super(), '__{}__'.format(op))(rhs)
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

    def __repr__(self):
        self._set_last_accessed()
        if self:  # dicts return True when not empty
            return super().__repr__()
        return str(self.id)


class Graph(Base):

    def _node_creator(graph):
        class NodeClass(Base):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.set_attr('id', graph._get_new_id())
                self.set_attr('sources', set())
                self.set_attr('destinations', set())

                graph._add_node(self)
        return NodeClass

    def _relation_creator(graph):
        class RelationClass(Base):
            def __init__(self, source, label, destination, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.set_attr('id', graph._get_new_id())
                self.set_attr('label', label)
                self.set_attr('source', source)
                self.set_attr('destination', destination)

                source.destinations.add(self)
                destination.sources.add(self)
                graph._add_relation(self)

            def __repr__(self):
                return str(self.label)
        return RelationClass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attr('_next_id', -1)  # Offset by one
        self.set_attr('id', self._get_new_id())
        self.set_attr('Node', self._node_creator())
        self.set_attr('Relation', self._relation_creator())
        self.set_attr('Search', self._search_creator())
        self.set_attr('nodes', set())
        self.set_attr('relations', set())
        self.set_attr('_cache', {})
        self.set_attr('data', {})
        self.data[0] = self

    def _get_new_id(self):
        self.set_attr('_next_id', self._next_id + 1)  # Offset by one
        return self._next_id

    def _add_node(self, node):
        self.nodes.add(node)
        self.data[node.id] = node
        self._cache['_stale'] = True
        return self

    def _add_relation(self, relation):
        self.relations.add(relation)
        self.data[relation.id] = relation
        self._cache['_stale'] = True
        return self

    def get_by_id(self, number):
        return self.data[number]

    def __getitem__(self, item):
        return self.get_by_id(item)

    # Some methods as defined by wikipedia [https://en.wikipedia.org/wiki/Graph_%28abstract_data_type%29]
    def adjacent(self, x, y):
        """One way search from x to y"""
        return any((y is relation.destination for relation in x.destinations))

    def adjacent_twoway(self, x, y):
        """Is x connected to y? (x->y or y->x)"""
        return self.adjacent(x, y) or self.adjacent(y, x)

    def neighbors(self, x):
        """ Get all neighbors that are destinations"""
        return [relation.destination for relation in x.destinations]

    def neighbors_twoway(self, x):
        """ Get all neighbors that are sources and destinations"""
        return [relation.destination for relation in x.destinations] + [relation.source for relation in x.sources]

    def remove_node(self, x):
        for relation in x.sources:
            relation.source.destinations.remove(relation)
            self.relations.remove(relation)
            self.data[relation.id] = None
            # del relation  # No effect, local scope
        del x.sources
        for relation in x.destinations:
            relation.destination.sources.remove(relation)
            self.relations.remove(relation)
            self.data[relation.id] = None
            # del relation  # No effect, local scope
        del x.destinations
        self.data[x.id] = None  # TODO change how deleted nodes are handled. will depend on persistance storage method
        self.nodes.remove(x)
        return self

    def _search_creator(graph):
        class Search(object):
            def __init__(self):
                self._search = graph.data.values()

            def property(self, prop):
                try:
                    self._search = (item for item in self._search if prop in item)
                except AttributeError:
                    self._search = (item for item in graph.data.values() if prop in item)
                finally:
                    return self

            def value(self, prop, value):
                try:
                    self._search = (item for item in self._search if item[prop] == value)
                except KeyError:
                    self._search = (item for item in self._search if prop in item and item[prop] == value)
                except AttributeError:
                    self._search = (item for item in self.get_by_propery(prop) if item[prop] == value)
                finally:
                    return self

            def relation_to(self, node, by=None):
                if by:
                    self._search = (relation.source for relation in node.sources if relation.lable is by)
                else:
                    self._search = (relation.source for relation in node.sources)
                return self

            def relation_from(self, node, by=None):
                if by:
                    self._search = (relation.destination for relation in node.destinations if relation.lable is by)
                else:
                    self._search = (relation.destination for relation in node.destinations)
                return self

            def relation(self, node, by=None):
                if by:
                    self._search = itertools.chain((relation.destination for relation in node.destinations if relation.lable is by),
                                                   (relation.source for relation in node.sources if relation.lable is by))
                else:
                    self._search = itertools.chain((relation.destination for relation in node.destinations),
                                                   (relation.source for relation in node.sources))
                return self

            def execute(self):
                try:
                    return list(self._search)
                except AttributeError:
                    return []

            @classmethod
            def get_by_propery(cls, prop):
                items = graph.data.values()
                return [item for item in items if prop in item]

            @classmethod
            def get_by_value(cls, prop, value):
                return [item for item in cls.get_by_propery(prop) if item[prop] == value]
        return Search
