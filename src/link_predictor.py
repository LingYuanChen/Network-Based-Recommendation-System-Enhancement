import networkx as nx
import pickle

category = "electronics"
directory = f"amazon_{category}_review/"

def predictLinksJaccard(GCombined, itemNodeIds, userNodeIds, directory):
    scores = {}

    for node1 in userNodeIds:
        try:
            neighbors1 = set(GCombined.neighbors(node1))
        except nx.NetworkXError:
            continue  # Skip the current iteration if node1 is not in the graph

        scores[node1] = {}
        for node2 in itemNodeIds:
            try:
                if not GCombined.has_node(node2) or GCombined.has_edge(node1, node2):
                    scores[node1][node2] = 0.0
                else:
                    neighbors2 = set(GCombined.neighbors(node2))
                    common_neighbors = neighbors1.intersection(neighbors2)
                    union_neighbors = neighbors1.union(neighbors2)
                    scores[node1][node2] = len(common_neighbors) / len(union_neighbors)
            except nx.NetworkXError:
                scores[node1][node2] = 0.0

    with open(directory + 'Jaccards', 'wb') as outfile:
        pickle.dump(scores, outfile)



def predictLinksNegatedShortestPath(GCombined, itemNodeIds, userNodeIds, directory):
    scores = {}

    for node1 in userNodeIds:
        for node2 in itemNodeIds:
            try:
                if not GCombined.has_node(node1) or not GCombined.has_node(node2) or GCombined.has_edge(node1, node2):
                    if node1 not in scores:
                        scores[node1] = {}
                    scores[node1][node2] = 0.0
                else:
                    try:
                        shortest_path_length = 1 / nx.shortest_path_length(GCombined, node1, node2)
                    except nx.NetworkXNoPath:
                        shortest_path_length = 0.0

                    if node1 not in scores:
                        scores[node1] = {}
                    scores[node1][node2] = shortest_path_length
            except nx.NetworkXError:
                scores[node1][node2] = 0.0

    with open(directory + 'NegatedShortestPath', 'wb') as outfile:
        pickle.dump(scores, outfile)

        
def predictLinksAdamicAdar(GCombined, itemNodeIds, userNodeIds, directory):
    scores = {}

    for node1 in userNodeIds:
        for node2 in itemNodeIds:
            try:
                if not GCombined.has_edge(node1, node2):
                    if not node1 in scores:
                        scores[node1] = {}
                    scores[node1][node2] = nx.adamic_adar_index(GCombined, [(node1, node2)])
                else:
                    if not node1 in scores:
                        scores[node1] = {}
                    scores[node1][node2] = 0.0
            except nx.NetworkXError:
                scores[node1][node2] = 0.0

    with open(directory + 'AdamicAdar', 'wb') as outfile:
        pickle.dump(scores, outfile)
        
def main():
    GCombined = nx.read_edgelist(f"amazon_{category}_review/GCombined_edgelist_{category}.txt")
    print("Finishing load the graph")
    itemNodeIds = [] 
    with open(directory + 'ItemNodeIds', 'rb') as infile1:
        itemNodeIds = pickle.load(infile1)
    userNodeIds = [] 
    with open(directory + 'UserNodeIds', 'rb') as infile1:
        userNodeIds = pickle.load(infile1)
    
    predictLinksJaccard(GCombined, itemNodeIds, userNodeIds, directory)
    print("Finishing Jaccard")
    predictLinksNegatedShortestPath(GCombined, itemNodeIds, userNodeIds, directory)
    print("Finishing NegatedShortestPath")
    predictLinksAdamicAdar(GCombined, itemNodeIds, userNodeIds, directory)
    print("Finishing AdamicAdar")
    

if __name__ == "__main__":
    main()