import unittest
import networkx as nx
import tempfile
import os
import json
from src.network_centrality import NetworkCentralityCalculator

class TestNetworkCentrality(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.test_dir, 'test_config.yaml')
        
        # Create test config
        test_config = {
            'paths': {
                'data_dir': 'data/',
                'output_dir': 'output/',
                'log_dir': 'logs/',
                'image_dir': 'image/'
            },
            'logging': {
                'level': 'INFO',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            }
        }
        
        with open(self.config_path, 'w') as f:
            json.dump(test_config, f)
            
        self.calculator = NetworkCentralityCalculator('test_category', self.config_path)
        
        # Create a test graph
        self.test_graph = nx.Graph()
        self.test_graph.add_edges_from([
            (1, 2), (2, 3), (3, 4), (4, 1),  # Square
            (2, 4), (1, 3)  # Cross diagonals
        ])

    def test_pagerank_calculation(self):
        """Test PageRank calculation."""
        pr = self.calculator.calculate_pagerank(self.test_graph)
        
        # Test properties of PageRank
        self.assertEqual(len(pr), len(self.test_graph))
        self.assertAlmostEqual(sum(pr.values()), 1.0, places=5)
        
        # All nodes should have similar PageRank due to symmetry
        pr_values = list(pr.values())
        self.assertAlmostEqual(max(pr_values), min(pr_values), places=5)

    def test_eigenvector_centrality(self):
        """Test eigenvector centrality calculation."""
        eigen = self.calculator.calculate_eigenvector_centrality(self.test_graph)
        
        # Test properties of eigenvector centrality
        self.assertEqual(len(eigen), len(self.test_graph))
        
        # Due to graph symmetry, all centralities should be equal
        eigen_values = list(eigen.values())
        self.assertAlmostEqual(max(eigen_values), min(eigen_values), places=5)

    def test_empty_graph(self):
        """Test handling of empty graphs."""
        empty_graph = nx.Graph()
        
        with self.assertRaises(Exception):
            self.calculator.calculate_pagerank(empty_graph)
            
        with self.assertRaises(Exception):
            self.calculator.calculate_eigenvector_centrality(empty_graph)

    def test_disconnected_graph(self):
        """Test handling of disconnected graphs."""
        disconnected_graph = nx.Graph()
        disconnected_graph.add_edges_from([
            (1, 2), (2, 3),  # Component 1
            (4, 5), (5, 6)   # Component 2
        ])
        
        # PageRank should work on disconnected graphs
        pr = self.calculator.calculate_pagerank(disconnected_graph)
        self.assertEqual(len(pr), 6)
        
        # Eigenvector centrality might raise an exception
        with self.assertRaises(Exception):
            self.calculator.calculate_eigenvector_centrality(disconnected_graph)

    def test_single_node_graph(self):
        """Test handling of single-node graphs."""
        single_node = nx.Graph()
        single_node.add_node(1)
        
        pr = self.calculator.calculate_pagerank(single_node)
        self.assertEqual(pr[1], 1.0)
        
        eigen = self.calculator.calculate_eigenvector_centrality(single_node)
        self.assertEqual(eigen[1], 1.0)

if __name__ == '__main__':
    unittest.main() 