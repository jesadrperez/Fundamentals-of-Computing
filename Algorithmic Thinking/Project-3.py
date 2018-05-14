# -*- coding: utf-8 -*-
"""
Created on Sun May 13 15:32:05 2018

@author: Adrian
"""

import alg_cluster
import Assignment_3 as assign
import random
import pandas as pd 
import numpy as np
import time
import gc


######################################################
# Question 1

def gen_random_clusters(num_clusters):
    '''
    Creates a list of clusters where each cluster in this list corresponds to 
    randomly, generated point in the square with corners (+- 1, +- 1).
    
    Input: num_clusters - the length of list of clusters
    
    Output: a list of length num_clusters of Clusters
    '''
    # Init list for storing clusters
    cluster_list = []
    # Loop over cluster_list till it is of length num_clusters
    while (len(cluster_list)) < num_clusters:
        # Randomly generate a point between (-1, 1) and save as x point
        horiz = random.uniform(-1,1)
        # Randomly generate a point between (-1, 1) and save as y point
        vert = random.uniform(-1,1)
        # Adds cluster to cluster_list
        cluster_list.append(alg_cluster.Cluster(set([]), horiz, vert, 0, 0))
    return cluster_list   

def compute_running_times():
    '''
    Computes the running time for slow_closest_pair() and fast_closest_pair() 
    for clusters of size 2 to 200.
    
    Input: NONE
    
    Output: a pandas df 
    '''
    # Disables garbage collection
    gc.disable()
    # Init cluster sizes
    num_clusters_list = np.arange(2, 201, 1)
    # Init list variables for storing run times
    slow_runtimes = []
    fast_runtimes = []
    # loop over cluster sizes
    for num_clusters in num_clusters_list:
        # Generate a cluster_list of size num_clusters
        clusters_list = gen_random_clusters(num_clusters)
        # Sort the cluster_list
        clusters_list.sort(key = lambda cluster: cluster.horiz_center())
        # Gets current time in seconds
        start_time = time.clock()
        # Perform slow clustering
        dummy_result = assign.slow_closest_pair(clusters_list)
        # Calculate runtime and store value
        slow_runtimes.append(time.clock() - start_time)
        # Gets current time in seconds
        start_time = time.clock()
        # Perform fast clustering
        dummy_result = assign.fast_closest_pair(clusters_list)
        # Calculate runtime and store value
        fast_runtimes.append(time.clock() - start_time)
    # create df from results
    return pd.DataFrame(dict({'slow':slow_runtimes, 'fast':fast_runtimes, 'num clusters': num_clusters_list}))

running_times_df = compute_running_times()
running_times_df.set_index('num clusters', inplace=True)
