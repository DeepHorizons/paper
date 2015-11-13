import itertools
import sys

import nodes


class Graph(object):

    def _node_creator(graph):
        class NodeClass(nodes.LazyLoadNode):
            def __init__(self, *args, **kwargs):
                super().__init__(id=graph._get_new_id(), *args)
                for prop in kwargs:
                    self[prop] = kwargs[prop]
                graph._add_node(self)

        return NodeClass

    def _relation_creator(graph):
        class RelationClass(nodes.LazyLoadRelation):
            def __init__(self, source, label, destination, *args, **kwargs):
                super().__init__(source, label, destination, id=graph._get_new_id(), *args)
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
        self._cache = {}
        self.data = {}

    def __sizeof__(self):
        return super().__sizeof__() + (sys.getsizeof(self._next_id) + sys.getsizeof(self.id) +
                                       sys.getsizeof(self._cache) + sys.getsizeof(self.data) +
                                       sum((sys.getsizeof(node) for node in self.data.values())))

    def _get_new_id(self):
        self._next_id += 1  # Offset by one
        return self._next_id

    def _add_node(self, node):
        self.data[object.__getattribute__(node, 'id')] = node
        self._cache.clear()
        return self

    def _add_relation(self, relation):
        self.data[relation.id] = relation
        self._cache.clear()
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
            self.data[relation.id] = None
            # del relation  # No effect, local scope
        for relation in x.destinations:
            relation.destination.sources.remove(relation)
            self.data[relation.id] = None
            # del relation  # No effect, local scope
        self.data[x.id] = None  # TODO change how deleted nodes are handled. will depend on persistance storage method
        x._remove()
        del x
        return self

    def remove_relation(self, relation):
        relation.source.destinations.remove(relation)
        relation.destination.source.remove(relation)
        del relation.source
        del relation.destination
        del relation.label
        self.data[relation.id] = None  # TODO change how deleted nodes are handled. will depend on persistance storage method
        return self

    def remove(self, item):
        try:
            item = self.data[item] if isinstance(item, int) else item
        except RecursionError:  # Item was already deleted
            return
        return self.remove_node(item) if isinstance(item, self.Node) else self.remove_relation(item) if isinstance(item, self.Relation) else None

    def _search_creator(graph):
        class Search(object):
            def __init__(self):
                self._search = graph.data.values()

            def _get_nodes(self):
                """Filters out everything but nodes from the search"""
                self._search = (node for node in self._search if isinstance(node, graph.Node))
                return self

            def _get_relations(self):
                """Filters out everything but relations from the search"""
                self._search = (relation for relation in self._search if isinstance(relation, graph.Relation))
                return self

            def _get_node_iterator(self, node):
                """Get an iterator of the node if set, otherwise look through all nodes"""
                return self._get_nodes()._search if not node else (graph.get_by_id(node),) if isinstance(node, int) else (node,)

            def _get_relation_iterator(self, relation):
                """Get an iterator of the relation if set, otherwise look through all nodes"""
                return self._get_relations()._search if not relation else (graph.get_by_id(relation),) if isinstance(relation, int) else (relation,)

            def property(self, prop):
                """Get all nodes that have the property"""
                self._search = (item for item in self._search if prop in item)
                return self

            def value(self, prop, value):
                """Get all nodes that have the property and that property is equal to the value"""
                self._search = (item for item in self._search if prop in item and item[prop] == value)
                return self

            def relations_to(self, node=None, by=None):
                """Get all nodes related to this node (source -> node)
                if no node it set, look through the list of nodes in the search
                if by is set, only get nodes that are related by that value"""
                if by:
                    self._search = (relation.source for _node in self._get_node_iterator(node) for relation in _node.sources if relation.label == by)
                else:
                    self._search = (relation.source for _node in self._get_node_iterator(node) for relation in _node.sources)
                return self

            def relations_from(self, node=None, by=None):
                """Get all nodes related to this node (node -> dest)
                if no node it set, look through the list of nodes in the search
                if by is set, only get nodes that are related by that value"""
                if by:
                    self._search = (relation.destination for _node in self._get_node_iterator(node) for relation in _node.destinations if relation.label == by)
                else:
                    self._search = (relation.destination for _node in self._get_node_iterator(node) for relation in _node.destinations)
                return self

            def relations(self, node=None, by=None):
                if by:
                    self._search = itertools.chain((relation.destination for _node in self._get_node_iterator(node) for relation in _node.destinations if relation.label == by),
                                                   (relation.source for _node in self._get_node_iterator(node) for relation in _node.sources if relation.label == by))
                else:
                    self._search = itertools.chain((relation.destination for _node in self._get_node_iterator(node) for relation in _node.destinations),
                                                   (relation.source for _node in self._get_node_iterator(node) for relation in _node.sources))
                return self

            def get_by_id(self, number):
                self._search = (item for item in (graph.get_by_id(int(number)),))
                return self

            def execute(self):
                """Execute the command"""
                return {node.id: node for node in self._search}

            @classmethod
            def get_by_propery(cls, prop):
                items = graph.data.values()
                return {item.id: item for item in items if prop in item}

            @classmethod
            def get_by_value(cls, prop, value):
                return {item.id: item for item in cls.get_by_propery(prop).values() if item[prop] == value}
        return Search
