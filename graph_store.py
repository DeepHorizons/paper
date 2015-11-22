import itertools
import sys

import nodes


class Graph(object):

    def _node_creator(graph):
        nodeclass = nodes.LiteNode if graph.lite else nodes.LazyLoadNode

        class NodeClass(nodeclass):
            def __init__(self, *args, **kwargs):
                super().__init__(id=graph._get_new_id(), *args)
                for prop in kwargs:
                    self[prop] = kwargs[prop]
                graph._add_node(self)
        return NodeClass

    def _relation_creator(graph):
        relationclass = nodes.LiteRelation if graph.lite else nodes.LazyLoadRelation

        class RelationClass(relationclass):
            def __init__(self, source, label, destination, *args, **kwargs):
                super().__init__(source, label, destination, id=graph._get_new_id(), *args)
                for prop in kwargs:
                    self[prop] = kwargs[prop]
                source.add_destination(self)
                destination.add_source(self)
                graph._add_relation(self)

        return RelationClass

    def __init__(self, *args, **kwargs):
        self.lite = kwargs.pop('lite', False)
        self.cache = kwargs.pop('cache', True)
        self.cache_max_length = kwargs.pop('max_length', float('inf'))

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
        self.data[object.__getattribute__(relation, 'id')] = relation
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
            relation.source.remove_destination(relation)
            self.data[relation.id] = None
            # del relation  # No effect, local scope
        for relation in x.destinations:
            relation.destination.remove_source(relation)
            self.data[relation.id] = None
            # del relation  # No effect, local scope
        self.data[x.id] = None  # TODO change how deleted nodes are handled. will depend on persistance storage method
        self._cache.clear()
        return self

    def remove_relation(self, relation):
        relation.source.remove_destination(relation)
        relation.destination.remove_source(relation)
        del relation.source
        del relation.destination
        del relation.label
        self.data[relation.id] = None  # TODO change how deleted nodes are handled. will depend on persistance storage method
        self._cache.clear()
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
                self._search = (item for item in self.property(prop)._search if item[prop] == value)
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
                search1, search2 = itertools.tee(self._search)
                self._search = search1
                relations_from = self.relations_from(node, by)._search
                self._search = search2  # Reset search as calling the relations_from functions sets the search
                self._search = itertools.chain(relations_from, self.relations_to(node, by)._search)
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

        if graph.cache:
            class SearchCache(Search):
                class CacheGenerator(object):
                    def __init__(self, cache, value, generator):
                        self.cache = cache
                        self.value = value
                        self.generator = generator
                        self.list = []
                        self.max_length = graph.cache_max_length

                    def __iter__(self):
                        return self

                    def __next__(self):
                        try:
                            item = next(self.generator)
                        except StopIteration as e:
                            if len(self.list) < self.max_length:
                                self.cache['result'] = self.list
                            raise e
                        else:
                            self.list.append(item)
                            return item

                def __init__(self):
                    super().__init__()
                    self.cache = graph._cache

                def _getiterator(self, key, gen):
                    if key in self.cache:
                        self.cache = self.cache[key]
                        if 'result' in self.cache:
                            return self.cache['result']
                        else:
                            return self.CacheGenerator(self.cache, key, gen)
                    else:
                        self.cache[key] = {}
                        self.cache = self.cache[key]
                        return self.CacheGenerator(self.cache, key, gen)

                def _get_nodes(self):
                    """Filters out everything but nodes from the search"""
                    key = (self._get_nodes.__name__)
                    gen = super()._get_nodes()._search
                    self._search = self._getiterator(key, gen)
                    return self

                def _get_relations(self):
                    """Filters out everything but relations from the search"""
                    key = (self._get_relations.__name__)
                    gen = super()._get_relations()._search
                    self._search = self._getiterator(key, gen)
                    return self

                def property(self, prop):
                    """Get all nodes that have the property"""
                    key = (self.property.__name__, prop)
                    gen = super().property(prop)._search
                    self._search = self._getiterator(key, gen)
                    return self

                def value(self, prop, value):
                    """Get all nodes that have the property and that property is equal to the value"""
                    key = (self.value.__name__, prop, value)
                    gen = super().value(prop, value)._search
                    self._search = self._getiterator(key, gen)
                    return self

                def relations_to(self, node=None, by=None):
                    """Get all nodes related to this node (source -> node)
                    if no node it set, look through the list of nodes in the search
                    if by is set, only get nodes that are related by that value"""
                    key = (self.relations_to.__name__, node, by)
                    gen = super().relations_to(node, by)._search
                    self._search = self._getiterator(key, gen)
                    return self

                def relations_from(self, node=None, by=None):
                    """Get all nodes related to this node (node -> dest)
                    if no node it set, look through the list of nodes in the search
                    if by is set, only get nodes that are related by that value"""
                    key = (self.relations_from.__name__, node, by)
                    gen = super().relations_from(node, by)._search
                    self._search = self._getiterator(key, gen)
                    return self

                def relations(self, node=None, by=None):
                    key = (self.relations.__name__, node, by)
                    gen = super().relations(node, by)._search
                    self._search = self._getiterator(key, gen)
                    return self
            return SearchCache
        return Search
