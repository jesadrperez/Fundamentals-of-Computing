# -*- coding: utf-8 -*-
"""
Created on Sun May 13 15:32:05 2018

@author: Adrian
"""

import alg_cluster
import Project_3 as project
import random
import pandas as pd 
import numpy as np
import time
import gc
import seaborn as sns
import alg_project3_viz as viz
import alg_clusters_matplotlib

sns.set_style("dark")


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
        dummy_result = project.slow_closest_pair(clusters_list)
        # Calculate runtime and store value
        slow_runtimes.append(time.clock() - start_time)
        # Gets current time in seconds
        start_time = time.clock()
        # Perform fast clustering
        dummy_result = project.fast_closest_pair(clusters_list)
        # Calculate runtime and store value
        fast_runtimes.append(time.clock() - start_time)
    # create df from results
    return pd.DataFrame(dict({'slow':slow_runtimes, 'fast':fast_runtimes, 'num clusters': num_clusters_list}))

def plot_Q1():
    '''
    Makes plot for Question 1
    '''
    # Generates the data
    running_times_df = compute_running_times()
    # Fixes index
    running_times_df.set_index('num clusters', inplace=True)   
    # plot the graph
    ax = running_times_df.plot.line(legend='best', 
                                    title='Running Times of Slow and Fast Closest Pairing Methods \n for Different Cluster Sizes.')
    # Add legend
    ax.legend(['Fast Closest Pair', 'Slow Closest Pair'])
    # Set lavels
    ax.set(xlabel='Number of Clusters',  ylabel='Seconds')
    # Add grid
    ax.grid(True)
    
    fig = ax.get_figure()
    fig.savefig('Application 3 - Q1.png')


######################################################
# Question 2
    
def plot_Q2():
    """
    Load a data table, compute a list of clusters and 
    plot a list of clusters

    Set DESKTOP = True/False to use either matplotlib or simplegui
    """
    DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
    DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
    
    data_table = viz.load_data_table(DATA_3108_URL)
    
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
        
    cluster_list = project.hierarchical_clustering(singleton_list, 15)
    print "Displaying", len(cluster_list), "hierarchical clusters"
           
    # draw the clusters using matplotlib
    alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, False)
    #alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)  #add cluster centers
    
    
######################################################
# Question 3
    
def plot_Q3():
    """
    Load a data table, compute a list of clusters and 
    plot a list of clusters

    Set DESKTOP = True/False to use either matplotlib or simplegui
    """
    DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
    DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
    
    data_table = viz.load_data_table(DATA_3108_URL)
    
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
        
    cluster_list = project.kmeans_clustering(singleton_list, 15, 5)	
    print "Displaying", len(cluster_list), "k-means clusters"
           
    # draw the clusters using matplotlib
    alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, False)
    #alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)  #add cluster centers    
    
    
######################################################
# Question 4


######################################################
# Question 5    
    
def plot_Q5():
    """
    Load a data table, compute a list of clusters and 
    plot a list of clusters

    Set DESKTOP = True/False to use either matplotlib or simplegui
    """
    DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
    DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"
    
    data_table = viz.load_data_table(DATA_111_URL)
    
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
        
    cluster_list = project.hierarchical_clustering(singleton_list, 9)
    print "Displaying", len(cluster_list), "hierarchical clusters"
           
    # draw the clusters using matplotlib
    alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, False)
    #alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)  #add cluster centers
    
######################################################
# Question 6    
    
def plot_Q6():
    """
    Load a data table, compute a list of clusters and 
    plot a list of clusters

    Set DESKTOP = True/False to use either matplotlib or simplegui
    """
    DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
    DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"
    
    data_table = viz.load_data_table(DATA_111_URL)
    
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
        
    cluster_list = project.kmeans_clustering(singleton_list, 9, 5)
    print "Displaying", len(cluster_list), "hierarchical clusters"
           
    # draw the clusters using matplotlib
    alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, False)
    #alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)  #add cluster centers
    
######################################################
# Question 7  
    
def cluster_data():
    '''
    Load a data table, compute a list of clusters and 
    
    Output: a tuple of two list of clusters (hierarchical, kmeans)
    '''
    DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
    DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"   
    DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
    
    data_table = viz.load_data_table(DATA_111_URL)
    
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
     
    singleton_list_copy = [cluster.copy() for cluster in singleton_list]
    
    return (project.hierarchical_clustering(singleton_list, 9), project.kmeans_clustering(singleton_list_copy, 9, 5))  

def compute_distortion(cluster_list):
    '''
    Computes the total distortion of a list of clusters.
    
    Input: cluster_list - a list of clusters.
    
    Output: total_distortion - a float of the total distortion
    '''
    
    DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
    DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"
    DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
    
    data_table = viz.load_data_table(DATA_111_URL)
    
    # Init list variable for storing distortion
    distortion = []
    # loop over clusters
    for cluster in cluster_list:
        # Calculate and save distortion
        distortion.append(cluster.cluster_error(data_table))
    return sum(distortion)        
    
def answer_Q7():
    '''
    Generates answer for question 7
    '''
    # Performs clustering
    data = cluster_data()
    # Computes distortion
    return (compute_distortion(data[0]), compute_distortion(data[1]))


######################################################
# Question 8 
    
######################################################
# Question 9
    
######################################################
# Question 10
    
def load_data(cancer_id):
    '''
    Loads the cancer data.
    
    Input: A string that denotes which cancer data to load
    
    Output: a tuple (data_table, cluster_list).
    '''
    
    DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
    data_url = DIRECTORY + "data_clustering/unifiedCancerData_" + cancer_id + ".csv"
    
    data_table = viz.load_data_table(data_url)
    
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
        
    return (data_table, singleton_list)

def compute_distortion_data_set(data_table, cluster_list):
    '''
    Computes the total distortion of a list of clusters.
    
    Input: data_set - a tuple (data_table, cluster_list).
    
    Output: total_distortion - a float of the total distortion
    '''
    # Init list variable for storing distortion
    distortion = []
    # loop over clusters
    for cluster in cluster_list:
        # Calculate and save distortion
        distortion.append(cluster.cluster_error(data_table))
    return sum(distortion) 


def test_clustering(data_set, method):
    '''
    Test the distortion of a data_set under clustering method.
    
    Input: a tuple (data_table, cluster_list) and a clustering algorithm 

    Output: a list of distortion values
    '''   
    # number of clusters to form
    num_cluster_list = np.arange(6,21,1)
    # init list to store distortion
    distortion_list = []
    # Loop over cluster sizes list
    for num_cluster in num_cluster_list:
        # make a copy of the cluster_list
        cluster_list = [cluster.copy() for cluster in data_set[1]] 
        if method == 'K-Means':
            # perfrom kmeans
            cluster_list = project.kmeans_clustering(cluster_list, num_cluster, 10)
        else:        
            # perform hier clustering
            project.hierarchical_clustering(cluster_list, num_cluster)
        # calculate and save distortion
        distortion_list.append(compute_distortion_data_set(data_set[0], cluster_list))
    return distortion_list

def generate_df(cancer_id):
    '''
    Plots the graph for cancer set 111.
    '''    
    # load data
    data_set = load_data(cancer_id)
    # Dict for storing values
    dist_dict = dict()
    # Add num_clusters
    dist_dict['Number of Clusters'] = np.arange(6,21,1)    
    # Compute distortion
    for method in ['K-Means', 'Hierarchical']: 
        # Computes distortion and saves values
        dist_dict[method] = test_clustering(data_set, method)        
    return pd.DataFrame(dist_dict).set_index('Number of Clusters')

def plot_q10():
    '''
    answer q10
    '''
    for cancer_id in ['111', '290', '896']:
        plot_df = generate_df(cancer_id)
        title = 'Distortion for Hierarchical and K-Means Cluster \n' + cancer_id + ' Cancer Dataset'
        ax = plot_df.plot.line(legend='best', title = title)
        ax.set(xlabel='Number of Clusters',  ylabel='Distortion')
        ax.grid(True)
        fig = ax.get_figure()
        fig.savefig('Application 3 - Q10_'+cancer_id+'.png')