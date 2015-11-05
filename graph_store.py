import itertools
import sys

import nodes


class Graph(object):

    def _node_creator(graph):
        class NodeClass(nodes.LazyLoadNode):
            def __init__(self, *args, **kwargs):
                super().__init__(graph._get_new_id(), *args)
                for prop in kwargs:
                    self[prop] = kwargs[prop]
                graph._add_node(self)

        return NodeClass

    def _relation_creator(graph):
        class RelationClass(nodes.LazyLoadRelation):
            def __init__(self, source, label, destination, *args, **kwargs):
                super().__init__(graph._get_new_id(), source, label, destination, *args)
                for prop in kwargs:
                    self[prop] = kwargs[prop]
                source.destinations.add(self)
                destination.sources.add(self)
                graph._add_relation(self)

            def __repr__(self):
                return str(self.label)
        return RelationClass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._next_id = -1  # Offset by one
        self.id = self._get_new_id()
        self.Node = self._node_creator()
        self.Relation = self._relation_creator()
        self.Search = self._search_creator()
        self.nodes = set()
        self.relations = set()
        self._cache = {}
        self.data = {}

    def _get_new_id(self):
        self._next_id += 1  # Offset by one
        return self._next_id

    def _add_node(self, node):
        self.nodes.add(node)
        self.data[node.id] = node
        self._cache.clear()
        return self

    def _add_relation(self, relation):
        self.relations.add(relation)
        self.data[relation.id] = relation
        self._cache.clear()
        return self

    def get_by_id(self, number):
        return self.data[number]

    def __getitem__(self, item):
        return self.get_by_id(item)

    def __sizeof__(self):
        return super().__sizeof__() + (sys.getsizeof(self._next_id) + sys.getsizeof(self.id) +
                                       sys.getsizeof(self._cache) + sys.getsizeof(self.data) +
                                       sum((sys.getsizeof(node) for node in self.data.values())))

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

            def _get_nodes(self):
                self._search = (node for node in self._search if type(node) is graph.Node)
                return self

            def _get_relations(self):
                self._search = (relation for relation in self._search if type(relation) is graph.Relation)
                return self

            def property(self, prop):
                """Get all nodes that have the property"""
                try:
                    self._search = (item for item in self._search if prop in item)
                except AttributeError:
                    self._search = (item for item in graph.data.values() if prop in item)
                finally:
                    return self

            def value(self, prop, value):
                """Get all nodes that have the property and that property is equal to the value"""
                try:
                    self._search = (item for item in self._search if prop in item and item[prop] == value)
                except AttributeError:
                    self._search = (item for item in self.get_by_propery(prop) if item[prop] == value)
                finally:
                    return self

            def relations_to(self, node=None, by=None):
                """Get all nodes related to this node (source -> node)
                if no node it set, look through the list of nodes in the search
                if by is set, only get nodes that are related by that value"""
                if node:
                    if type(node) is int:
                        node = graph.get_by_id(node)
                    if by:
                        self._search = (relation.source for relation in node.sources if relation.label is by)
                    else:
                        self._search = (relation.source for relation in node.sources)
                else:
                    self._get_nodes()
                    if by:
                        self._search = (relation.source for _node in self._search for relation in _node.sources if relation.label is by)
                    else:
                        self._search = (relation.source for _node in self._search for relation in _node.sources)
                return self

            def relations_from(self, node=None, by=None):
                """Get all nodes related to this node (node -> dest)
                if no node it set, look through the list of nodes in the search
                if by is set, only get nodes that are related by that value"""
                if node:
                    if type(node) is int:
                        node = graph.get_by_id(node)
                    if by:
                        self._search = (relation.destination for relation in node.destinations if relation.label is by)
                    else:
                        self._search = (relation.destination for relation in node.destinations)
                else:
                    self._get_nodes()
                    if by:
                        self._search = (relation.destination for _node in self._search for relation in _node.destinations if relation.label is by)
                    else:
                        self._search = (relation.destination for _node in self._search for relation in _node.destinations)
                return self

            def relations(self, node=None, by=None):
                if node:
                    if type(node) is int:
                        node = graph.get_by_id(node)
                    if by:
                        self._search = itertools.chain((relation.destination for relation in node.destinations if relation.label is by),
                                                       (relation.source for relation in node.sources if relation.label is by))
                    else:
                        self._search = itertools.chain((relation.destination for relation in node.destinations),
                                                       (relation.source for relation in node.sources))
                else:
                    self._get_nodes()
                    if by:
                        self._search = itertools.chain((relation.destination for _node in self._search for relation in _node.destinations if relation.label is by),
                                                       (relation.source for _node in self._search for relation in _node.sources if relation.label is by))
                    else:
                        self._search = itertools.chain((relation.destination for _node in self._search for relation in _node.destinations),
                                                       (relation.source for _node in self._search for relation in _node.sources))
                return self

            def execute(self):
                """Execute the command"""
                try:
                    return {node.id: node for node in self._search}
                except AttributeError:
                    return {}

            @classmethod
            def get_by_propery(cls, prop):
                items = graph.data.values()
                return [item for item in items if prop in item]

            @classmethod
            def get_by_value(cls, prop, value):
                return [item for item in cls.get_by_propery(prop) if item[prop] == value]
        return Search
