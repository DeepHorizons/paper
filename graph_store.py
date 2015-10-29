
class Base(dict):
    _next_id = -1

    @staticmethod
    def _get_new_id():
        Base._next_id += 1
        return Base._next_id

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().__setattr__('id', Base._get_new_id())

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
                self.set_attr('sources', [])  # TODO make this a set
                self.set_attr('destinations', [])  # TODO make this a set

                graph._add_node(self)
        return NodeClass

    def Relation(graph):
        class RelationClass(Base):
            def __init__(self, source, destination, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.set_attr('source', source)
                self.set_attr('destination', source)

                source.destinations.append(self)
                destination.sources.append(self)
                graph._add_relation(self)
        return RelationClass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_attr('Node', self.Node())
        self.set_attr('Relation', self.Relation())
        self.set_attr('nodes', {})
        self.set_attr('relations', {})
        self.set_attr('data', {})

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
