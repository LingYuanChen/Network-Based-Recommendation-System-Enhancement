import networkx as nx
import json
import time
import sys


category = sys.argv[1]

graphList = ['GItems', 'GUsers']
directory = f"amazon_{category}_review/"  

for graph in graphList:
    
    # Load graph
    G = nx.read_edgelist(directory+f"{graph}_edgelist_{category}.txt")
    dict1 = {}
    
    # Function to calculate PageRank for a subgraph
    pr = nx.pagerank(G)

    with open(directory + f"Pagerank_{graph}_{category}.json", 'w') as outfile1:
        json.dump(pr, outfile1)
    
    print("Finish Pagerank")

    eigen = nx.eigenvector_centrality(G)

    with open(directory + f"Eigen_Value_{graph}_{category}.json", 'w') as outfile2:
        json.dump(eigen, outfile2)
    print("Finish eigenvector_centrality")