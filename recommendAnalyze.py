from sys import argv
import gzip
import json
import pickle
import json
from matplotlib import pyplot
import os
import random

category = argv[1]
directory = f"amazon_{category}_review/"
graph = 'GUsers'
year = argv[2]
month = argv[3]
rate = argv[4]
rec_num = argv[5]

# weeks = range(int(week)+1,int(week)+13)

newEdges = {} # Ground truth next year

def parseIterator(path):
    g = gzip.open(path, 'r')
    for l in g:
        yield eval(l)
        

        
def findNewEdges():
    with open(directory + 'Dictionary_Items_' + category + '.txt', 'r') as f1:
        asinItems = json.load(f1)
    with open(directory + 'Dictionary_Users_' + category + '.txt', 'r') as f2:
        reviewerIdUsers = json.load(f2)
    
    filename = f"{directory}amazon_{category}_reviews_{year}_{month}.json.gz"
    for review in parseIterator(filename):
        # print review['reviewerID']
        if review['reviewerID'] in reviewerIdUsers: # Check if user in the years we predicted from
            nodeNumber = reviewerIdUsers[review['reviewerID']]
            if not nodeNumber in newEdges:
                newEdges[nodeNumber] = []
            itemNodeId = int(asinItems[review['asin']])
            newEdges[nodeNumber].append(itemNodeId)
                
def checkEdges(communities,community_keys, userToItems):
    with open(directory + 'recommendations','rb') as f:
        predictions = pickle.load(f)

    allScores = []
    allPreds = []
    allUsers = []
    for cluster in range(0, len(predictions)):
        # print(len(predictions))
        commScores = []
        commPreds = []
        commUsers = 0.0
        item_user = set()
        for userStr, items in predictions[cluster].items():
            user = int(userStr)
            if not user in newEdges:
                groundTruth = set()
            else:
                groundTruth = set(newEdges[user])
            
            
            # for u in communities[community_keys[cluster]]:
            #     item_user.update(userToItems[u])
            # # print(item_user)
            # try:itemSet = set(random.sample(list(item_user), 10))
            # except:
            #     itemSet = set(random.sample(range(0,98294), 10))
            #     pass
            
            itemSet = set(items)
            matched = set.intersection(*[itemSet, groundTruth])
            if len(itemSet) == 0:
                score = 0.5
                continue
            else:
                score = len(matched)*1.0/len(itemSet)
            if score>1: print(matched,itemSet)
            commScores.append(score)
            commPreds.append(len(itemSet))
            commUsers += 1
        allScores.append(commScores)
        allUsers.append(commUsers)
        allPreds.append(commPreds)

    commScores = [sum(x)*100.0/(0.000001+len(x)) for x in allScores]
    # print("allscore:",allScores[0],len(allScores[0]),sum(allScores[0]),sum(allScores[0])*100.0/(0.000001+len(allScores[0])))
    # print("commScores", commScores)
    commPreds = [sum(x)/(0.000001+len(x)) for x in allPreds]
    X = [commScores[i]*allUsers[i] for i in range(len(allUsers))]
    # print zip(commScores, commPreds)
    # print allUsers
    reslt = sum(X)/sum(allUsers)
    string = f'Year: {year} Score: {reslt}'
    print(string) 
    pyplot.plot(range(len(predictions)), commScores, 'b-', label = 'Correct')
    #pyplot.plot(range(len(predictions)), commPreds, 'r--', label = 'Correct')
    pyplot.title('Cluster vs. Percentage of Predictions')
    pyplot.xlabel('Cluster')
    with open(directory+'../finalResults.txt', 'a') as myfile:
        myfile.write(string+'\n')
    pyplot.ylabel('Percentage of Correct Predictions')
    pyplot.legend(loc = 'upper right')
    # pyplot.show()
    pyplot.savefig(f'{directory}pic/{rate}_{rec_num}.png')

def main(argv):
    with open(directory+f"{graph}_communities_louvain_{category}.json",'r') as f1:
            communities = json.load(f1)
    userToItems = {}
    with open(directory + '_User_Item_' + category + '.txt', 'r') as infile4:
        userToItems = json.load(infile4)
    community_keys = list(communities.keys())
    findNewEdges()
    checkEdges(communities, community_keys, userToItems)

if __name__ == '__main__':
    main(argv)