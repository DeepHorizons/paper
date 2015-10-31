import datetime


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

    def Node(graph):
        class NodeClass(Base):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.set_attr('id', graph._get_new_id())
                self.set_attr('sources', set())
                self.set_attr('destinations', set())

                graph._add_node(self)
        return NodeClass

    def Relation(graph):
        class RelationClass(Base):
            def __init__(self, source, destination, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.set_attr('id', graph._get_new_id())
                self.set_attr('source', source)
                self.set_attr('destination', destination)

                source.destinations.add(self)
                destination.sources.add(self)
                graph._add_relation(self)
        return RelationClass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attr('_next_id', -1)  # Offset by one
        self.set_attr('id', self._get_new_id())
        self.set_attr('Node', self.Node())
        self.set_attr('Relation', self.Relation())
        self.set_attr('nodes', {})
        self.set_attr('relations', {})
        self.set_attr('data', {})

    def _get_new_id(self):
        self.set_attr('_next_id', self._next_id + 1)  # Offset by one
        return self._next_id

    def _add_node(self, node):
        self.nodes[node.id] = node

    def _add_relation(self, relation):
        self.relations[relation.id] = relation

    def get_by_id(self, number):
        if self.id == number:
            r = self
        elif number in self.nodes.keys():
            r = self.nodes[number]
        elif number in self.relations.keys():
            r = self.relations[number]
        else:
            raise LookupError('id {} does not exist'.format(number))
        return r

    def __getitem__(self, item):
        return self.get_by_id(item)

    # Some methods as defined by wikipedia [https://en.wikipedia.org/wiki/Graph_%28abstract_data_type%29]
    def adjacent(self, x, y):
        """One way search from x to y"""
        for relation in x.destinations:
            if y is relation.destination:
                return True
        return False

    def adjacent_twoway(self, x, y):
        """Is x connected to y? (x->y or y->x)"""
        if self.adjacent(x, y) or self.adjacent(y, x):
            return True
        return False

    def neighbors(self, x):
        return [relation.destination for relation in x.destinations]

    def neighbors_twoway(self, x):
        return [relation.destination for relation in x.destinations] + [relation.source for relation in x.sources]

    def remove_node(self, x):
        for relation in x.sources:
            relation.source.destinations.remove(relation)
            x.sources.remove(relation)
            del relation
        for relation in x.destinations:
            relation.destination.sources.remove(relation)
            x.destinations.remove(relation)
            del relation
        del x

    def search_for_property(self, property):
        items = list(self.nodes.values()) + list(self.relations.values())
        return [item for item in items if property in item]

    def search_for_value(self, property, value):
        return [item for item in self.search_for_property(property) if item[property] == value]
