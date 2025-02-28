import networkx as nx
import json
import time
import logging
from collections import defaultdict
from infomap import Infomap
import community
import sys
import yaml
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/community_detector.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CommunityDetector:
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
            f"{self.directory}/GItemsCommunities",
            f"{self.directory}/GUsersCommunities",
            "logs"
        ]
        for d in dirs:
            Path(d).mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {d}")

    def detect_communities_infomap(self, G):
        """Detect communities using Infomap algorithm."""
        try:
            infomap = Infomap("--two-level")
            # Add links to the Infomap object
            for edge in G.edges():
                infomap.addLink(int(edge[0]), int(edge[1]))

            # Run the Infomap algorithm
            infomap.run()
            
            # Get the communities
            communities = defaultdict(list)
            for node in infomap.iterTree():
                if node.isLeaf():
                    communities[node.moduleIndex()].append(node.physicalId)
                    
            logger.info(f"Detected {len(communities)} communities using Infomap")
            return dict(communities)
            
        except Exception as e:
            logger.error(f"Error in Infomap community detection: {e}")
            raise

    def detect_communities_louvain(self, G):
        """Detect communities using Louvain method."""
        try:
            partition = community.best_partition(G)
            logger.info(f"Completed Louvain method for graph with {len(G.nodes())} nodes")

            communities = defaultdict(list)
            for node, comm_id in partition.items():
                communities[comm_id].append(node)

            logger.info(f"Detected {len(communities)} communities using Louvain")
            return dict(communities)
            
        except Exception as e:
            logger.error(f"Error in Louvain community detection: {e}")
            raise

    def write_communities(self, communities, graph):
        """Write community data to files."""
        try:
            for key, members in communities.items():
                filename = f"{self.directory}{graph}Communities/{graph}Community{key}"
                with open(filename, 'w') as file:
                    for item in members:
                        file.write(f"{item}\n")
            logger.info(f"Wrote {len(communities)} communities to files for {graph}")
            
        except Exception as e:
            logger.error(f"Error writing communities to files: {e}")
            raise

    def process_graph(self, graph_name):
        """Process a single graph for community detection."""
        try:
            logger.info(f"Processing {graph_name}")
            G = nx.read_edgelist(f"{self.directory}{graph_name}_edgelist_{self.category}.txt")
            
            # Detect communities using Louvain method
            communities_louvain = self.detect_communities_louvain(G)
            
            # Save results
            with open(f"{self.directory}{graph_name}_communities_louvain_{self.category}.json", 'w') as f:
                json.dump(communities_louvain, f)
            
            # Write individual community files
            self.write_communities(communities_louvain, graph_name)
            
            logger.info(f"Completed processing {graph_name}")
            
        except Exception as e:
            logger.error(f"Error processing {graph_name}: {e}")
            raise

    def run(self):
        """Run community detection on all graphs."""
        start_time = time.time()
        
        try:
            for graph in self.graph_list:
                self.process_graph(graph)
                
            end_time = time.time()
            logger.info(f"Total processing time: {end_time - start_time:.2f} seconds")
            
        except Exception as e:
            logger.error(f"Error in community detection pipeline: {e}")
            raise

def main():
    try:
        category = sys.argv[1]
        detector = CommunityDetector(category)
        detector.run()
    except Exception as e:
        logger.error(f"Error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()