
class Base(dict):
    def set_attr(self, key, value):
        """Access to the set attr method since we overwrite it"""
        super().__setattr__(key, value)

    def __hash__(self):
        return self.id

    def __setitem__(self, key, value):
        return super().__setitem__(key, value)

    def __setattr__(self, key, value):
        return self.__setitem__(key, value)

    def __getitem__(self, item):
        return super().__getitem__(item)

    def __getattr__(self, item):
        return self.__getitem__(item)


class Graph(Base):

    def Node(graph):
        class NodeClass(Base):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.set_attr('id', graph._get_new_id())
                self.set_attr('sources', [])  # TODO make this a set
                self.set_attr('destinations', [])  # TODO make this a set

                graph._add_node(self)
        return NodeClass

    def Relation(graph):
        class RelationClass(Base):
            def __init__(self, source, destination, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.set_attr('id', graph._get_new_id())
                self.set_attr('source', source)
                self.set_attr('destination', destination)

                source.destinations.append(self)
                destination.sources.append(self)
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
