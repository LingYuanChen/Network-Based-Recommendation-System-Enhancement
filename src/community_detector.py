import networkx as nx
import json
import time
from collections import defaultdict
from infomap import Infomap
import community
import sys


category = sys.argv[1]
# Function to calculate PageRank for a subgraph
graphList = ['GItems', 'GUsers']
directory = f"amazon_{category}_review/"  


def communities_Infomap(G):
    infomap = Infomap("--two-level")
    # Add links to the Infomap object
    for edge in G.edges():
        infomap.addLink(int(edge[0]), int(edge[1]))

    # Run the Infomap algorithm
    infomap.run()

    # Get the communities from the Infomap object
    communities = {}
    for node in infomap.iterTree():
        if node.isLeaf():
            community = node.moduleIndex()
            if community not in communities:
                communities[community] = []
            communities[community].append(node.physicalId)
    return communities
    
    
def communities_Louvian(G):
    # Louvain method
    partition = community.best_partition(G)
    print(f"finish Louvain method {G}")

    # Convert the community results to separate dictionaries using defaultdict
    communities_louvain = defaultdict(list)

    # Assign nodes to communities in separate dictionaries
    for node, comm_id in partition.items():
        communities_louvain[comm_id].append(node)
    return communities_louvain


def writefile(communities,graph):
    for key in communities.keys():
        fileName = directory+ f"{graph}Communities/{graph}Community{key}"
        file = open(fileName, 'w')
        for item in communities[key]:
            file.write("%s\n" % item)
    
def main():
    # load Itemgraph and User graph
    for graph in graphList:
        G = nx.read_edgelist(directory+f"{graph}_edgelist_{category}.txt")
        communities_louvain = communities_Louvian(G)
        # communities_infomap = communities_Infomap(G)
        
        # wrtie graph community into json file
        with open(directory+f"{graph}_communities_louvain_{category}.json",'w') as f1:
            json.dump(communities_louvain,f1)
        f1.close()


if __name__== "__main__":
    main()