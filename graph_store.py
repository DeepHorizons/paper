
class Base(dict):
    _next_id = -1

    @staticmethod
    def _get_new_id():
        Base._next_id += 1
        return Base._next_id

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = Base._get_new_id()

    def __hash__(self):
        return self.id

    # TODO Fix all of these
    def __setitem__(self, key, value):
        if hasattr(self, 'id'):
            print('set item')
            return super().__setitem__(key, value)
        else:
            return super().__setitem__(key, value)

    # TODO Fix all of these
    def __setattr__(self, key, value):
        if hasattr(self, 'id'):
            print('set attr')
            return self.__setitem__(key, value)
        else:
            return super().__setattr__(key, value)

    # TODO Fix all of these
    def __getitem__(self, item):
        if hasattr(self, 'id'):
            print('get item')
            return super().__getitem__(item)
        else:
            return super().__getitem__(item)

    # TODO Fix all of these
    def __getattr__(self, item):
        try:
            self.id
        except:
            return super().__getattribute__(item)
        else:
            print('get attr')
            return self.__getitem__(item)


class Graph(Base):
    def Node(graph):
        class NodeClass(Base):
            def __init__(self, *args, **kwargs):
                self.sources = []  # TODO make this a set
                self.destinations = []  # TODO make this a set
                super().__init__(*args, **kwargs)

                graph._add_node(self)
        return NodeClass

    def Relation(graph):
        class RelationClass(Base):
            def __init__(self, source, destination, *args, **kwargs):
                self.source = source
                self.destination = destination
                super().__init__(*args, **kwargs)

                source.destinations.append(self)
                destination.sources.append(self)
                graph._add_relation(self)
        return RelationClass

    def __init__(self, *args, **kwargs):
        self.Node = self.Node()
        self.Relation = self.Relation()
        self.nodes = {}
        self.relations = {}
        self.data = {}
        super().__init__(*args, **kwargs)

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
