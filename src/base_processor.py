import logging
import yaml
from pathlib import Path
import networkx as nx
import json
from typing import List, Dict, Any

class BaseProcessor:
    """Base class for all processors in the recommendation system."""
    
    def __init__(self, category: str, config_path: str = 'config/config.yaml'):
        self.category = category
        self.config = self._load_config(config_path)
        self.directory = f"amazon_{category}_review/"
        self.setup_directories()
        self.logger = self._setup_logger()

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise RuntimeError(f"Error loading config file: {e}")

    def _setup_logger(self) -> logging.Logger:
        """Setup logging for the processor."""
        logger = logging.getLogger(self.__class__.__name__)
        log_file = Path(self.config['paths']['log_dir']) / f"{self.__class__.__name__.lower()}.log"
        
        formatter = logging.Formatter(
            self.config['logging']['format']
        )
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        logger.setLevel(self.config['logging']['level'])
        
        return logger

    def setup_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        dirs = [
            self.directory,
            Path(self.config['paths']['log_dir']),
            Path(self.config['paths']['output_dir']),
            Path(self.config['paths']['data_dir']),
            Path(self.config['paths']['image_dir'])
        ]
        for d in dirs:
            Path(d).mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Created directory: {d}")

    def load_graph(self, graph_name: str) -> nx.Graph:
        """Load a graph from edgelist file."""
        try:
            path = f"{self.directory}{graph_name}_edgelist_{self.category}.txt"
            G = nx.read_edgelist(path)
            self.logger.info(f"Loaded graph {graph_name} with {len(G.nodes())} nodes and {len(G.edges())} edges")
            return G
        except Exception as e:
            self.logger.error(f"Error loading graph {graph_name}: {e}")
            raise

    def save_json(self, data: Dict, filename: str) -> None:
        """Save data to JSON file."""
        try:
            with open(f"{self.directory}/{filename}", 'w') as f:
                json.dump(data, f)
            self.logger.info(f"Saved data to {filename}")
        except Exception as e:
            self.logger.error(f"Error saving JSON file {filename}: {e}")
            raise

    def load_json(self, filename: str) -> Dict:
        """Load data from JSON file."""
        try:
            with open(f"{self.directory}/{filename}", 'r') as f:
                data = json.load(f)
            self.logger.info(f"Loaded data from {filename}")
            return data
        except Exception as e:
            self.logger.error(f"Error loading JSON file {filename}: {e}")
            raise 