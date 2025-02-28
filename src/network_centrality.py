import networkx as nx
import json
import time
import logging
import sys
import yaml
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/network_centrality.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class NetworkCentralityCalculator:
    def __init__(self, category, config_path='config/config.yaml'):
        self.category = category
        self.config = self._load_config(config_path)
        self.directory = f"amazon_{category}_review/"
        self.graph_list = ['GItems', 'GUsers']
        self.setup_directories()

    def _load_config(self, config_path):
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading config file: {e}")
            raise

    def setup_directories(self):
        """Create necessary directories if they don't exist."""
        dirs = [
            self.directory,
            "logs"
        ]
        for d in dirs:
            Path(d).mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {d}")

    def calculate_pagerank(self, G):
        """Calculate PageRank for a graph."""
        try:
            pr = nx.pagerank(G)
            logger.info("PageRank calculation completed")
            return pr
        except Exception as e:
            logger.error(f"Error calculating PageRank: {e}")
            raise

    def calculate_eigenvector_centrality(self, G):
        """Calculate eigenvector centrality for a graph."""
        try:
            eigen = nx.eigenvector_centrality(G)
            logger.info("Eigenvector centrality calculation completed")
            return eigen
        except Exception as e:
            logger.error(f"Error calculating eigenvector centrality: {e}")
            raise

    def process_graph(self, graph_name):
        """Process a single graph for centrality metrics."""
        try:
            logger.info(f"Processing {graph_name}")
            
            # Load graph
            G = nx.read_edgelist(f"{self.directory}{graph_name}_edgelist_{self.category}.txt")
            logger.info(f"Loaded graph {graph_name} with {len(G.nodes())} nodes and {len(G.edges())} edges")
            
            # Calculate PageRank
            pr = self.calculate_pagerank(G)
            with open(f"{self.directory}Pagerank_{graph_name}_{self.category}.json", 'w') as outfile:
                json.dump(pr, outfile)
            
            # Calculate eigenvector centrality
            eigen = self.calculate_eigenvector_centrality(G)
            with open(f"{self.directory}Eigen_Value_{graph_name}_{self.category}.json", 'w') as outfile:
                json.dump(eigen, outfile)
                
            logger.info(f"Completed processing {graph_name}")
            
        except Exception as e:
            logger.error(f"Error processing {graph_name}: {e}")
            raise

    def run(self):
        """Run centrality calculations on all graphs."""
        start_time = time.time()
        
        try:
            for graph in self.graph_list:
                self.process_graph(graph)
                
            end_time = time.time()
            logger.info(f"Total processing time: {end_time - start_time:.2f} seconds")
            
        except Exception as e:
            logger.error(f"Error in centrality calculation pipeline: {e}")
            raise

def main():
    try:
        category = sys.argv[1]
        calculator = NetworkCentralityCalculator(category)
        calculator.run()
    except Exception as e:
        logger.error(f"Error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()