import unittest
import tempfile
import shutil
import os
from pathlib import Path
import networkx as nx
import json
from src.base_processor import BaseProcessor

class TestBaseProcessor(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
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
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'file': 'test.log'
            }
        }
        
        with open(self.config_path, 'w') as f:
            json.dump(test_config, f)
            
        self.processor = BaseProcessor('test_category', self.config_path)

    def tearDown(self):
        # Remove the temporary directory and its contents
        shutil.rmtree(self.test_dir)

    def test_directory_creation(self):
        """Test that all required directories are created."""
        expected_dirs = [
            'amazon_test_category_review',
            'logs',
            'data',
            'output',
            'image'
        ]
        
        for dir_name in expected_dirs:
            dir_path = Path(self.test_dir) / dir_name
            self.assertTrue(dir_path.exists(), f"Directory {dir_name} was not created")
            self.assertTrue(dir_path.is_dir(), f"{dir_name} is not a directory")

    def test_graph_operations(self):
        """Test graph loading and saving operations."""
        # Create a test graph
        G = nx.Graph()
        G.add_edges_from([(1, 2), (2, 3), (3, 4)])
        
        # Save the graph
        graph_path = os.path.join(self.test_dir, 'test_graph.txt')
        nx.write_edgelist(G, graph_path)
        
        # Load the graph
        loaded_G = self.processor.load_graph('test_graph')
        
        self.assertEqual(len(G.nodes()), len(loaded_G.nodes()))
        self.assertEqual(len(G.edges()), len(loaded_G.edges()))

    def test_json_operations(self):
        """Test JSON file operations."""
        test_data = {'key': 'value', 'number': 42}
        filename = 'test.json'
        
        # Save JSON
        self.processor.save_json(test_data, filename)
        
        # Load JSON
        loaded_data = self.processor.load_json(filename)
        
        self.assertEqual(test_data, loaded_data)

    def test_error_handling(self):
        """Test error handling for invalid operations."""
        # Test loading non-existent graph
        with self.assertRaises(Exception):
            self.processor.load_graph('nonexistent_graph')
        
        # Test loading non-existent JSON
        with self.assertRaises(Exception):
            self.processor.load_json('nonexistent.json')

if __name__ == '__main__':
    unittest.main() 