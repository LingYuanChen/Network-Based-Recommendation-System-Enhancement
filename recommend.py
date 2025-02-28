import json
import networkx as nx
from os import listdir
from os.path import isfile, join
from sys import argv
import pickle
import math


category = argv[1]
N = int(argv[2]) # How many predictions per user
directory = f"amazon_{category}_review/"
graph = 'GUsers'


usersGraph = nx.read_edgelist(directory+f"GUsers_edgelist_{category}.txt")
print(f"Finish loading usersGraph:{usersGraph}")
itemsGraph = nx.read_edgelist(directory+f"GItems_edgelist_{category}.txt")
print(f"Finish loading itemsGraph:{itemsGraph}")
GCombined = nx.read_edgelist(directory+f"GCombined_edgelist_{category}.txt")
print(f"Finish loading GCombinedGraph:{GCombined}")



# Read in page rank scores 
pagerank = {}
with open(directory + f"Pagerank_{graph}_{category}.json", 'r') as infile1:
    pagerank = json.load(infile1)

print("Finish loading pagerank")
# Read in eigen centrality scores 
eigen_centrality = {}
with open(directory + f"Eigen_Value_{graph}_{category}.json", 'r') as infile2:
    eigen_centrality = json.load(infile2)
print("Finish loading eigen_centrality")
def nodes_at_hop(graph,category):
    usersGraph = nx.read_edgelist(directory+f"{graph}_edgelist_{category}.txt")
    print(f"Finish reading graph at nodes_at_hop:{usersGraph}")
    communities = {}
    with open(directory+f"{graph}_communities_louvain_{category}.json",'r') as f1:
            communities = json.load(f1)
    print("Finish loading community")
    matrix ={}
    if graph == "Gusers": BATCH_SIZE = 1
    else: BATCH_SIZE = 100
    for community_idx, nodes in communities.items():
        G = usersGraph.subgraph(nodes)
        if int(community_idx)%BATCH_SIZE == 0:print(f"Finish creating {graph}subgraph_{community_idx}_{G}")
        matrix[community_idx] = dict()

        for node in nodes:
            distances = nx.single_source_shortest_path_length(G, node)

            matrix[community_idx][node]= distances
    return matrix



# Read in userNodeIds
userNodeIds = [] 
with open(directory + 'UserNodeIds', 'rb') as infile1:
    userNodeIds = pickle.load(infile1)



# Read in itemNodeIds 
itemNodeIds = [] 
with open(directory + 'ItemNodeIds', 'rb') as infile1:
    itemNodeIds = pickle.load(infile1)

print("Finish loading itemNodeIds")
# Read in nodeToAmazonIds
with open(directory + 'NodeIdToAmazonId','r') as f1:
    nodeToAmazonIds = json.load(f1)
f1.close()
print("Finish loading nodeToAmazonIds")
# Read in amazonIdsToNodeIds
with open(directory + 'AmazonIdToCombinedId', 'r') as f2:
    AmazonIdToCombinedId = json.load(f2)
f2.close()
print("Finish loading AmazonIdToCombinedId")

# nodesAtHopItems = []
# for filename in inFiles:
#     with open(inputDirectoryItems + filename, 'r') as infile4:
#         curCluster = json.load(infile4)
#     nodesAtHopItems.append(curCluster)

userToItems = {}
with open(directory + '_User_Item_' + category + '.txt', 'r') as infile4:
    userToItems = json.load(infile4)

print("Finish loading userToItems")

# PR, EIG
wtVec = [2.0, 1.5]

def dotProduct(vec):
    score = 0
    for idx in range(len(wtVec)):
        score += wtVec[idx]*vec[idx]
    return score

def updateDict(scores, hopDistance, queryUser, targetUser, items, alreadyBought):
    scale = 1.0/hopDistance
    pr = pagerank[targetUser]
    eig = eigen_centrality[targetUser]
    numThrownAway = 0
    for item in items:
        if item in alreadyBought:
            numThrownAway += 1
            continue
        if not item in scores:
            scores[item] = 0.0
        scores[item] += scale*dotProduct([pr,eig])
    # print 100.0*numThrownAway/len(items)
    return


print("Start loading nodesAtHopItems")
nodesAtHopItems = nodes_at_hop("GItems", category)
print("Finish loading nodesAtHopItems")
itemToCommunityDict = {} 
for community in nodesAtHopItems:
    for item in nodesAtHopItems[community]:
        if not item in itemToCommunityDict:
            itemToCommunityDict[item] = set()
        itemToCommunityDict[item].update(nodesAtHopItems[community].keys())
print("Finish loading itemToCommunityDict")
# print itemToCommunityDict.keys()
itemWeight = 5.0
def updateByItemCommunity(scores, distance, referenceItems, alreadyBought):
    scale = 1/(1.0+distance)
    for item in referenceItems:
        # print item
        if item not in itemToCommunityDict:
            continue
        simItems = itemToCommunityDict[item]
        # print simItems
        for simItem in simItems:
            # print simItem
            if simItem in alreadyBought:
                continue
            if not simItem in scores:
                scores[simItem] = 0.0
            scores[simItem] += scale*itemWeight
            # print simItem
print("Start loading nodesAtHop")
nodesAtHop = nodes_at_hop(graph, category)
print("Finish loading nodesAtHop")
# userRecommendations = []
# c = 0
# for community,nodes in nodesAtHop.items():
#     if c ==1:break
#     # print(nodes)
#     for i,j in nodes.items():
#         for a,b in j.items():
#             print(a,b)
#     c+=1

userRecommendations = []
for community in nodesAtHop:
    if int(community)%10 == 0: print(community)
    userRecommendations.append({})
    # print(nodesAtHop[community])
    for queryUser in nodesAtHop[community]:
        # print(queryUser, nodesAtHop[community][queryUser])
        scores = {} # Item -> Score
        allNbrs = nodesAtHop[community][queryUser]
        alreadyBought = userToItems[queryUser]
        for targetUser in allNbrs:
            if queryUser == targetUser: continue
            boughtItems = userToItems[targetUser]
            hopDistance = allNbrs[targetUser]
            # print(hopDistance)
            # print(community,queryUser,targetUser,hopDistance, alreadyBought, boughtItems)
            
            updateDict(scores, hopDistance, queryUser, targetUser, boughtItems, alreadyBought)
            updateByItemCommunity(scores, hopDistance, boughtItems, alreadyBought)
        updateByItemCommunity(scores, 0, alreadyBought, alreadyBought)
        srted = sorted(scores.items(), key=lambda x:(-x[1],x[0]))
        topN = [x[0] for x in srted[:min(N,len(srted))]]
        userRecommendations[-1][queryUser] = topN
 
print("Start saving Recommendations")       
with open(directory + 'recommendations', 'wb') as outfile:
    pickle.dump(userRecommendations, outfile)

# print(userRecommendations)
