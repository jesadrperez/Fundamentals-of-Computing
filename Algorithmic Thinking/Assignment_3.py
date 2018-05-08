"""
Student template code for Project 3
Student will implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane
"""

import math
import alg_cluster


######################################################
# Code for closest pairs of clusters

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters
    
    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    # initalize output
    output = (float("inf"), -1, -1)   
    # generate all indexex of clusters
    cluster_indexes = range(len(cluster_list))
    # loop over cluster_list
    for first_cluster in cluster_indexes:
        #print 'first cluster:', first_cluster
        # get remaining clusters in cluster_index
        remaining_cluster_indexes = cluster_indexes[first_cluster+1:]
        # loop over remaining clusters
        for second_cluster in remaining_cluster_indexes:
            #print 'second cluster:', second_cluster
            # compute pair disance between pairs
            dist_tuple = pair_distance(cluster_list, first_cluster, second_cluster)
            # compare to smallest known distance
            if dist_tuple[0] < output[0]:
                # replace smallest known distance            
                output = dist_tuple
    return output



def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    # get the number of clusters in cluster_list
    num_clusters = len(cluster_list)
    # Use slow_closest_pair if more efficeient
    if num_clusters <= 3:
        output = slow_closest_pair(cluster_list)
    # Use (fast) recusive method 
    else:
        # find the center of the list
        center_of_list = num_clusters/2
        # seperate clusters into left and right
        left_cluster_list = cluster_list[:center_of_list]
        right_cluster_list = cluster_list[center_of_list:]
        # find the closest pair in the left list
        left_dist = fast_closest_pair(left_cluster_list)
        # find the closest pair in the right
        right_dist = fast_closest_pair(right_cluster_list)
        # Compare left and right dist        
        if left_dist[0] < right_dist[0]:
            # Left dist is smaller
            output = left_dist                  
        else:
            # right dist is smaller
            output = (right_dist[0], right_dist[1]+center_of_list, right_dist[2]+center_of_list)
        # Compute horiz_center - center line strip
        horiz_center = (cluster_list[num_clusters-1] + cluster_list[num_clusters])
        # Compute closest pair strip
        closest_output = closest_pair_strip(cluster_list, horiz_center, output[0])
        # ADD COMMENT
        if output[0] > closest_output[0]:
            output = closest_output       
    return output


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.       
    """
    # copy cluster list
    copy_cluster_list = cluster_list[:]
    # sort copy cluster_list by vertical coordinates       
    copy_cluster_list.sort(key = lambda cluster: cluster.vert_center())
    # creates set for storing indices
    index_set = set([])
    # loops over cluster_list by index
    for index in range(len(copy_cluster_list)):
        # calculates the abs difference between cluster at index and horiz_center
        abs_diff = abs(copy_cluster_list[index].horiz_center() - horiz_center)
        # Compares abs_diff and half_width
        if abs_diff < half_width:
        # Adds index to set
            index_set.add(index)
    #print 'index_set:', index_set
    # get the length of index_set
    set_length = len(index_set)
    # default output for comparison
    output = (float('inf'), -1, -1)
    # first loop
    for dummy_u in range(0, set_length - 1):
       # print 'u:', dummy_u
        for dummy_v in range(dummy_u + 1, min(dummy_u + 3, set_length)):
            #print 'v:', dummy_v
            dist = pair_distance(copy_cluster_list, list(index_set)[dummy_u], list(index_set)[dummy_v])
            if dist[0] < output[0]:
                output = dist       
    return output
 
    
######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    
    return []


######################################################################
# Code for k-means clustering

    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """

    # position initial clusters at the location of clusters with largest populations
            
    return []

