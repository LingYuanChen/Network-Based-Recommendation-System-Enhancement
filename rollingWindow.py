import pandas as pd
import numpy as np
import json
import gzip
import os
import sys
import snap
import time
import math 
from os import listdir
from os.path import isfile, join
import shutil
from collections import Counter
from collections import defaultdict
import pickle
import matplotlib.pyplot as plt
from scipy.stats import norm, expon, powerlaw, lognorm
import matplotlib.cm as cm
import matplotlib.colors as colors
import networkx as nx
import itertools
import sys

GItems = nx.Graph()
userEdges = Counter()
asinItems = {} # Key (string) is the asin of the item and value is the nodeId (int) in the graph
nodeItems = {}

GUsers = nx.Graph()

nodeIdUsers = {} # Key is the nodeId (int) in the graph and value (string) is the reviewerID of the user
reviewerIdUsers = {} # Key (string) is the reviewerID of the user and value is the nodeId (int) in the graph

GCombined = nx.Graph()
combinedNodeId = 0
combinedDict1 = {} # Maps nodeIds to AmazonIds
combinedDict2 = {} # Maps AmazonIds to nodeIds
category = sys.argv[1]
rate = int(sys.argv[2])

directory = f"amazon_{category}_review/"


def parseIterator(path):
    g = gzip.open(path, 'r')
    for l in g:
        yield eval(l)

def split_reviews_by_year(input_file, item):
    output_directory = f"amazon_{item}_review" 

    with gzip.open(input_file, 'rt') as f:
        for line in f:
            review = json.loads(line)
            review_month = int(review['reviewTime'].split(' ')[-3]) # Extract the year from the 'reviewTime' field
            review_year = int(review['reviewTime'].split(' ')[-1])
            if review_year== 2013 or review_year== 2012 or review_year== 2011:
                output_file = os.path.join(output_directory, f'amazon_{item}_reviews_2011_2013.json.gz')

                with gzip.open(output_file, 'at') as output:
                    output.write(json.dumps(review) + '\n')
            if review_year== 2014 and review_month <=9:
                output_file = os.path.join(output_directory, f'amazon_{item}_reviews_2011_2013.json.gz')

                with gzip.open(output_file, 'at') as output:
                    output.write(json.dumps(review) + '\n')
                    
def groundTruth_month(input_file, item):
    output_directory = f"amazon_{item}_review" 

    with gzip.open(input_file, 'rt') as f:
        for line in f:
            review = json.loads(line)
            review_month = int(review['reviewTime'].split(' ')[-3]) # Extract the year from the 'reviewTime' field
            review_year = int(review['reviewTime'].split(' ')[-1])
            if review_year== 2014 and review_month<= 12 and review_month> 9:
                print("review_month")
                output_file = os.path.join(output_directory, f'amazon_{item}_reviews_2014_101112.json.gz')

                with gzip.open(output_file, 'at') as output:
                    output.write(json.dumps(review) + '\n')
        
        
def parseItems(path):
    global combinedNodeId
    itemsNodeId = 0 
    edges = set()
    BATCH_SIZE = 1000000 # Adjust the batch size as needed
    batch_count = 0
    for item in parseIterator(path):
        if batch_count % BATCH_SIZE == 0:
            print(batch_count)
        GItems.add_node(itemsNodeId)
        GCombined.add_node(itemsNodeId)
        asinItems[item['asin']] = itemsNodeId
        nodeItems[itemsNodeId] = item['asin']
        combinedDict1[itemsNodeId] = item['asin']
        combinedDict2[item['asin']] = itemsNodeId
        itemsNodeId +=1
        batch_count +=1
        try:
            related = item['related']
            bought_together = set(related['bought_together'])
            edges.update((item['asin'], item_dst_asin) for item_dst_asin in bought_together)
        except KeyError:
            pass
    print(f"Finished adding item nodes to GItems:{GItems}")   
    print(f"Finished adding item nodes to GCombined:{GCombined}")
    updated_edges = []
    for edge in edges:
        try:
            updated_edges.append((asinItems[edge[0]], asinItems[edge[1]]))
        except KeyError:
            pass

    GItems.add_edges_from(updated_edges)
    GCombined.add_edges_from(updated_edges)
    combinedNodeId = itemsNodeId
    itemNodeIds = [i for i in range(0, combinedNodeId)]
    with open(directory + 'ItemNodeIds', 'wb') as outfile:
        pickle.dump(itemNodeIds, outfile)
        
    with open(directory + 'Dictionary_Items_' + category + '.txt', 'w') as f1:
        json.dump(asinItems, f1)
    print(f"Finished adding item edges to {GItems}")
    print(f"Finished adding item edges to {GCombined}")

        
def parseReviews(path, goodRating):
    global combinedNodeId
    usersNodeId = 0
    userNodeIds = [] 
    reviewerIdUsers = {}
    reviewersByAsin = defaultdict(list)
    userToItems = defaultdict(list)
    nodeIdToCombinedNodeId = {}
    BATCH_SIZE = 1000000  # Adjust the batch size as needed
    batch_count = 0
    for review in parseIterator(path):
        if batch_count % BATCH_SIZE == 0:
            print(batch_count)
        reviewerId = reviewerIdUsers.get(review['reviewerID'])
        if reviewerId is None:
            GUsers.add_node(usersNodeId)
            GCombined.add_node(combinedNodeId)
            nodeIdToCombinedNodeId[usersNodeId] = combinedNodeId
            nodeIdUsers[usersNodeId] = review['reviewerID']
            reviewerIdUsers[review['reviewerID']] = usersNodeId
            combinedDict1[combinedNodeId] = review['reviewerID']
            combinedDict2[review['reviewerID']] = combinedNodeId
            userNodeIds.append(usersNodeId)
            usersNodeId += 1
            combinedNodeId += 1
            
    
        
        rating = review['overall']
        if rating >= goodRating:
            user = reviewerIdUsers[review['reviewerID']]
            asin = review['asin']
            
            reviewersByAsin[asin].append((user, rating))
            userToItems[user].append(asinItems[asin])
            # add user-item edges 
            GCombined.add_edge(nodeIdToCombinedNodeId[user], asinItems[asin])
            
        batch_count +=1
    
    print(f"Finished adding nodes to {GCombined}")
    print("reviewersByAsin:", len(reviewersByAsin))
    
    
    BATCH_SIZE = 1000000  # Adjust the batch size as needed
    batch_count = 0


    for _, users in reviewersByAsin.items():
        if batch_count % BATCH_SIZE == 0:
            print(batch_count)
        if len(users) < 2:
            batch_count += 1
            continue

        combinations = itertools.combinations(users, 2)  # Use combinations as a generator

        for user1, user2 in combinations:
            GUsers.add_edge(user1[0], user2[0])
            GCombined.add_edge(nodeIdToCombinedNodeId[user1[0]], nodeIdToCombinedNodeId[user2[0]])

        batch_count += 1
    print(f"Finished adding user edges to GUsers: {GUsers}")
    print(f"Finished adding user edges to GCombined:{GCombined}")
    
    with open(directory+'NodeIdToAmazonId','w') as f1:
        json.dump(combinedDict1,f1)
    f1.close()
    with open(directory+'AmazonIdToCombinedId','w') as f2:
        json.dump(combinedDict2,f2)
    f2.close()
    
    with open(directory + 'Dictionary_Users_' + category + '.txt', 'w') as f1:
        json.dump(reviewerIdUsers, f1)
    f1.close()
    with open(directory + '_User_Item_' + category + '.txt', 'w') as f:
        json.dump(userToItems, f)
    f.close()
    with open(directory + 'UserNodeIds', 'wb') as outfile:
        pickle.dump(userNodeIds, outfile)
    outfile.close()

def storeGraph(item):
    filename = directory+f"GItems_edgelist_{item}.txt"
    nx.write_edgelist(GItems, filename)
    
    print("Finishing: Store the GItems in a text file.")
    filename = directory+f"GUsers_edgelist_{item}.txt"
    nx.write_edgelist(GUsers, filename)
    print("Finishing: Store the GUsers in a text file.")
    
    filename = directory+f"GCombined_edgelist_{item}.txt"
    nx.write_edgelist(GCombined, filename)
    print("Finishing: Store the GCombined in a text file.")

    
    
def main():
    
    input_file_path = f"amazon_{category}_review/data/{category}_5.json.gz"
    split_reviews_by_year(input_file_path, category)
    groundTruth_month(input_file_path, category)

    parseItems(directory + f"data/meta_{category}.json.gz")
    
    print("Finishing parseItems ")
    combined_review = directory+f"amazon_{category}_reviews_2011_2013.json.gz"
    parseReviews(combined_review, rate)
 
    
    print("Finishing parseReviews ")
    
    storeGraph(category)
    print("Finishing: Store the graph in a text file.")
    
    
    
    


if __name__ == '__main__':
    # Start the timer
    start_time = time.time()
    

    main()
    
    # Stop the timer
    end_time = time.time()
    
    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    # Print the total time taken
    print(f"Total time taken: {elapsed_time} seconds")