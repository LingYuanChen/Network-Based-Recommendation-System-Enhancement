import unittest
import networkx as nx

class TestGraphConstruction(unittest.TestCase):
    def setUp(self):
        self.G = nx.Graph()
        
    def test_graph_creation(self):
        """Test if graph can be created and modified"""
        self.G.add_node(1)
        self.G.add_node(2)
        self.G.add_edge(1, 2)
        
        self.assertEqual(len(self.G.nodes), 2)
        self.assertEqual(len(self.G.edges), 1)
        
    def test_graph_properties(self):
        """Test basic graph properties"""
        self.G.add_nodes_from([1, 2, 3, 4])
        self.G.add_edges_from([(1, 2), (2, 3), (3, 4)])
        
        self.assertTrue(nx.is_connected(self.G))
        self.assertEqual(nx.number_of_nodes(self.G), 4)
        
if __name__ == '__main__':
    unittest.main() 