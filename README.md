# Amazon Product Recommendation System

This project implements a graph-based recommendation system using Amazon product review data. It analyzes user-item interactions and product relationships to generate personalized recommendations through various network analysis techniques.

## Project Structure

- `parseGraph.py`: Initial data processing and graph construction
- `rollingWindow.py`: Time-based analysis with rolling window approach
- `communityDetection.py`: Community detection using Infomap and Louvain methods
- `centrality.py`: Network centrality analysis
- `linkPrediction.py`: Link prediction for recommendations
- `recommendAnalyze.py`: Analysis of recommendation results
- `delete_file.py`: Utility script for cleanup
- `run.sh`: Shell script to run the complete pipeline

## Features

- Graph-based representation of user-item interactions
- Multiple recommendation algorithms:
  - Jaccard similarity
  - Negated shortest path
  - Adamic-Adar index
- Community detection using:
  - Louvain method
  - Infomap algorithm
- Network centrality metrics:
  - PageRank
  - Eigenvector centrality
- Time-based analysis with rolling windows
- Performance evaluation metrics

## Requirements

- Python 3.x
- Required Python packages:
  - networkx
  - infomap
  - community
  - pandas
  - numpy
  - matplotlib
  - scipy
  - snap
  - pickle

## Data Structure

The system expects Amazon review data in the following format:
- Product metadata in `meta_{category}.json.gz`
- Review data in `{category}_5.json.gz`
- Data should be placed in `amazon_{category}_review/data/` directory

## Usage

1. Prepare your data in the required format and directory structure
2. Set the category and parameters in `run.sh`
3. Execute the pipeline:
```bash
./run.sh
```

The pipeline will:
1. Parse and construct graphs
2. Perform community detection
3. Calculate centrality metrics
4. Generate recommendations
5. Analyze and evaluate results

## Parameters

- `category`: Product category (e.g., 'electronics', 'musical_instruments')
- `rate`: Minimum rating threshold for considering positive interactions
- `rec_num`: Number of recommendations to generate per user

## Output

The system generates:
- Graph files in edgelist format
- Community detection results
- Centrality metrics
- Recommendation scores and predictions
- Performance analysis plots in the `pic` directory
- Results summary in `finalResults.txt`

## Directory Structure

```
amazon_{category}_review/
├── data/
│   ├── meta_{category}.json.gz
│   └── {category}_5.json.gz
├── pic/
└── [generated files and results]
```

## Performance Evaluation

The system evaluates recommendations using:
- Prediction accuracy
- Community-based metrics
- Time-based validation
- Visualization of results

Results are stored in:
- PNG files for visualizations
- JSON files for detailed metrics
- Text files for summary statistics

## License

[Specify your license here]

## Contributors

[Add contributors here] 