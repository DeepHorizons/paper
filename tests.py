import graph_store
import unittest
import time


class TestGraphStore(unittest.TestCase):
    def setUp(self):
        self.g = graph_store.Graph()

    def test_graph_properties(self):
        self.assertEqual(self.g.id, 0)

    def test_node_creation(self):
        node = self.g.Node()
        self.assertEqual(node.id, 1)
        self.assertIn(node.id, self.g.data)
        self.assertEqual(node, self.g[1])
        self.assertEqual(node, self.g.get_by_id(1))

    def test_node_properties(self):
        node = self.g.Node(test3=3.14)
        node['test1'] = 5
        self.assertEqual(node['test1'], 5)
        node.test2 = 'a'
        self.assertEqual(node.test2, 'a')
        self.assertEqual(node['test2'], 'a')
        self.assertEqual(node.test1, 5)
        self.assertEqual(node['test1'], 5)
        self.assertEqual(node.test3, 3.14)
        self.assertEqual(node['test3'], 3.14)

    def test_relation_creation(self):
        node1 = self.g.Node()
        node2 = self.g.Node()
        r = self.g.Relation(node1, 'TEST', node2)
        self.assertEqual(r.id, 3)
        self.assertIn(r.id, self.g.data)
        self.assertEqual(r, self.g[3])
        self.assertEqual(r, self.g.get_by_id(3))

    def test_relation_properties(self):
        node1 = self.g.Node()
        node2 = self.g.Node()
        r = self.g.Relation(node1, 'TEST', node2, test1=1.68)
        r.test2 = 'value'
        r['test3'] = 'blah'

        self.assertEqual(r.label, 'TEST')
        self.assertEqual(r.test1, 1.68)
        self.assertEqual(r['test1'], 1.68)
        self.assertEqual(r.test2, 'value')
        self.assertEqual(r['test2'], 'value')
        self.assertEqual(r.test3, 'blah')
        self.assertEqual(r['test3'], 'blah')

    def test_node_relation(self):
        node1 = self.g.Node()
        node2 = self.g.Node()
        r = self.g.Relation(node1, 'TEST', node2)

        self.assertIs(node1, r.source)
        self.assertIs(node2, r.destination)
        self.assertIn(r, node1.destinations)
        self.assertIn(r, node2.sources)

    def test_node_deletion(self):
        graph = self.g
        node1 = graph.Node()
        node2 = graph.Node()
        node2.test = 1
        node3 = graph.Node()
        node4 = graph.Node()
        r1 = graph.Relation(node1, 'TEST', node2)
        r2 = graph.Relation(node1, 'TEST', node3)
        r3 = graph.Relation(node2, 'TEST', node3)
        r4 = graph.Relation(node2, 'TEST', node4)
        r5 = graph.Relation(node2, 'TEST', node1)

        graph.remove_node(node2)

        # Test that the node was removed
        self.assertNotIn(node2, self.g.data)

        # Test that relations were removed
        self.assertNotIn(r1, self.g.data)
        self.assertNotIn(r1, node1.destinations)

        self.assertNotIn(r3, self.g.data)
        self.assertNotIn(r3, node3.sources)

        self.assertNotIn(r4, self.g.data)
        self.assertNotIn(r4, node4.sources)

        self.assertNotIn(r5, self.g.data)
        self.assertNotIn(r5, node1.sources)

        self.assertIn(r2.id, self.g.data)
        self.assertIn(node1.id, self.g.data)
        self.assertIn(node3.id, self.g.data)
        self.assertIn(node4.id, self.g.data)

    def test_adjacent(self):
        node1 = self.g.Node()
        node2 = self.g.Node()

        self.assertFalse(self.g.adjacent(node1, node2))
        self.assertFalse(self.g.adjacent(node2, node2))
        self.assertFalse(self.g.adjacent_twoway(node1, node2))
        self.assertFalse(self.g.adjacent_twoway(node2, node1))

        self.g.Relation(node1, 'TEST', node2)

        self.assertTrue(self.g.adjacent(node1, node2))
        self.assertFalse(self.g.adjacent(node2, node2))
        self.assertTrue(self.g.adjacent_twoway(node1, node2))
        self.assertTrue(self.g.adjacent_twoway(node2, node1))

        self.g.Relation(node2, 'TEST', node1)

        self.assertTrue(self.g.adjacent(node1, node2))
        self.assertTrue(self.g.adjacent(node2, node1))
        self.assertTrue(self.g.adjacent_twoway(node1, node2))
        self.assertTrue(self.g.adjacent_twoway(node2, node1))

    def test_neighbors(self):
        node1 = self.g.Node()
        node2 = self.g.Node()
        node3 = self.g.Node()
        node4 = self.g.Node()

        self.g.Relation(node1, 'TEST', node2)
        self.g.Relation(node2, 'TEST', node3)
        self.g.Relation(node3, 'TEST', node4)
        self.g.Relation(node4, 'TEST', node1)

        neighbors = self.g.neighbors(node2)

        self.assertIn(node3, neighbors)
        self.assertNotIn(node1, neighbors)
        self.assertNotIn(node4, neighbors)

        neighbors = self.g.neighbors_twoway(node2)

        self.assertIn(node3, neighbors)
        self.assertIn(node1, neighbors)
        self.assertNotIn(node4, neighbors)

    def test_node_access_time(self):
        node = self.g.Node()
        node2 = self.g.Node()
        starttime = node._last_accessed
        time.sleep(0.1)
        self.assertEqual(node._last_accessed, starttime)
        _ = 1 == node
        self.assertGreater(node._last_accessed, starttime)

        starttime = node._last_accessed
        time.sleep(0.01)
        _ = node == 1
        self.assertGreater(node._last_accessed, starttime)

        starttime = node._last_accessed
        time.sleep(0.01)
        _ = 'test' in node
        self.assertEqual(node._last_accessed, starttime)
        # TODO add more coverage

        starttime = node._last_accessed
        starttime2 = node2._last_accessed
        time.sleep(0.01)
        _ = node == node2
        self.assertGreater(node._last_accessed, starttime)
        self.assertGreater(node2._last_accessed, starttime2)

        starttime = node._last_accessed
        starttime2 = node2._last_accessed
        time.sleep(0.01)
        _ = node2 == node
        self.assertGreater(node._last_accessed, starttime)
        self.assertGreater(node2._last_accessed, starttime2)


class TestGraphStoreLite(unittest.TestCase):
    def setUp(self):
        self.g = graph_store.Graph(lite=True)

    def test_graph_properties(self):
        self.assertEqual(self.g.id, 0)

    def test_node_creation(self):
        node = self.g.Node()
        self.assertEqual(node.id, 1)
        self.assertIn(node.id, self.g.data)
        self.assertEqual(node, self.g[1])
        self.assertEqual(node, self.g.get_by_id(1))

    def test_node_properties(self):
        node = self.g.Node(test3=3.14)
        node['test1'] = 5
        self.assertEqual(node['test1'], 5)
        node.test2 = 'a'
        self.assertEqual(node.test2, 'a')
        self.assertEqual(node['test2'], 'a')
        self.assertEqual(node.test1, 5)
        self.assertEqual(node['test1'], 5)
        self.assertEqual(node.test3, 3.14)
        self.assertEqual(node['test3'], 3.14)

    def test_relation_creation(self):
        node1 = self.g.Node()
        node2 = self.g.Node()
        r = self.g.Relation(node1, 'TEST', node2)
        self.assertEqual(r.id, 3)
        self.assertIn(r.id, self.g.data)
        self.assertEqual(r, self.g[3])
        self.assertEqual(r, self.g.get_by_id(3))

    def test_relation_properties(self):
        node1 = self.g.Node()
        node2 = self.g.Node()
        r = self.g.Relation(node1, 'TEST', node2, test1=1.68)
        r.test2 = 'value'
        r['test3'] = 'blah'

        self.assertEqual(r.label, 'TEST')
        self.assertEqual(r.test1, 1.68)
        self.assertEqual(r['test1'], 1.68)
        self.assertEqual(r.test2, 'value')
        self.assertEqual(r['test2'], 'value')
        self.assertEqual(r.test3, 'blah')
        self.assertEqual(r['test3'], 'blah')

    def test_node_relation(self):
        node1 = self.g.Node()
        node2 = self.g.Node()
        r = self.g.Relation(node1, 'TEST', node2)

        self.assertIs(node1, r.source)
        self.assertIs(node2, r.destination)
        self.assertIn(r, node1.destinations)
        self.assertIn(r, node2.sources)


    def test_adjacent(self):
        node1 = self.g.Node()
        node2 = self.g.Node()

        self.assertFalse(self.g.adjacent(node1, node2))
        self.assertFalse(self.g.adjacent(node2, node2))
        self.assertFalse(self.g.adjacent_twoway(node1, node2))
        self.assertFalse(self.g.adjacent_twoway(node2, node1))

        self.g.Relation(node1, 'TEST', node2)

        self.assertTrue(self.g.adjacent(node1, node2))
        self.assertFalse(self.g.adjacent(node2, node2))
        self.assertTrue(self.g.adjacent_twoway(node1, node2))
        self.assertTrue(self.g.adjacent_twoway(node2, node1))

        self.g.Relation(node2, 'TEST', node1)

        self.assertTrue(self.g.adjacent(node1, node2))
        self.assertTrue(self.g.adjacent(node2, node1))
        self.assertTrue(self.g.adjacent_twoway(node1, node2))
        self.assertTrue(self.g.adjacent_twoway(node2, node1))

    def test_neighbors(self):
        node1 = self.g.Node()
        node2 = self.g.Node()
        node3 = self.g.Node()
        node4 = self.g.Node()

        self.g.Relation(node1, 'TEST', node2)
        self.g.Relation(node2, 'TEST', node3)
        self.g.Relation(node3, 'TEST', node4)
        self.g.Relation(node4, 'TEST', node1)

        neighbors = self.g.neighbors(node2)

        self.assertIn(node3, neighbors)
        self.assertNotIn(node1, neighbors)
        self.assertNotIn(node4, neighbors)

        neighbors = self.g.neighbors_twoway(node2)

        self.assertIn(node3, neighbors)
        self.assertIn(node1, neighbors)
        self.assertNotIn(node4, neighbors)




if __name__ == '__main__':
    unittest.main()
