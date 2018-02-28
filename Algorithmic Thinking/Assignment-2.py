# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 19:38:05 2018

@author: Adrian

In this Application, we will analyze the connectivity of a computer network as 
it undergoes a cyber-attack. In particular, we will simulate an attack on this 
network in which an increasing number of servers are disabled. In 
computational terms, we will model the network by an undirected graph and 
repeatedly delete nodes from this graph. We will then measure the resilience 
of the graph in terms of the size of the largest remaining connected component 
as a function of the number of nodes deleted.
"""

# general imports
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import random
import numpy as np
import urllib2
import time
import math
from collections import deque
import seaborn as sns
import gc



############################################
# Provided code for Application portion of Module 2

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order  

##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

###################################
# Code for generating undirected graphs

def make_complete_graph(num_nodes):
    '''
    Takes the number of nodes and returns a dictionary corresponding to a 
    complete undirected graph with the specified number of nodes. 
    '''    
    # Creates an empty graph dict
    ugraph = dict()
    # Adds all nodes to dict with no edges
    for node in range(num_nodes):
        ugraph[node] = set()
    # Computes all pairwise permutations
    node_pairs = itertools.combinations(range(num_nodes), 2)
    # Loops over all pairwise permutations
    for node_i, node_j in node_pairs:
        # Adds an edge from node_i to node_j
        ugraph[node_i].add(node_j)
        # Adds an edge from node_j to node_i
        ugraph[node_j].add(node_i) 
    return ugraph
    
def algorithm_ER(num_nodes, prob):
    '''
    Computes a random undirected graph with num_nodes, where the likelihood 
    that two nodes (i,j) have an edge from i to j with probability prob. 
    Returns a dict representation of generated graph.
    '''
    # Creates an empty graph dict
    ugraph = dict()
    # Adds all nodes to dict with no edges
    for node in range(num_nodes):
        ugraph[node] = set()   
    # Computes all pairwise permutations
    node_pairs = itertools.combinations(range(num_nodes), 2)
    # Loops over all pairwise permutations
    for node_i, node_j in node_pairs:
        # Calculates a random uniform value
        chance = random.uniform(0, 1)
        # Checks if chance is less than prob
        if chance < prob:
            # Adds an edge from node_i to node_j
            ugraph[node_i].add(node_j)
            # Adds an edge from node_j to node_i
            ugraph[node_j].add(node_i)
    return ugraph

class UPATrial:
    """
    Provided code for application portion of module 2. Helper class for 
    implementing efficient version of UPA algorithm.
    
    Simple class to encapsulate optimizated trials for the UPA algorithm
    
    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are in the same proportion as 
    the desired probabilities.
    
    Use random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_nodes trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that each node number
        appears in correct ratio
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        for dummy_idx in range(len(new_node_neighbors)):
            self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors

def algorithm_UPA(num_nodes, node_connection):
    '''
    Generates a synthetic undirected graph with num_nodes. First a complete 
    directed graph is generated on node_connection nodes. Then, the graph is 
    grown by adding num_nodes - node_connection nodes. Where each new node is 
    connected to node_connection nodes randomly chosen from the set of existing
    nodes.
    Returns a dictionary of the digraph.
    '''
    # Makes a complete graph with node_connection nodes
    ugraph = make_complete_graph(node_connection)
    # Loads provided class for chosing subset nodes
    node_chooser = UPATrial(node_connection)
    # Adds missing nodes (num_nodes - node_connection nodes)
    for added_node in range(node_connection, num_nodes):
        # Chooses node_connection subet of nodes
        choosen_nodes = node_chooser.run_trial(node_connection)
        # Adds an edge between added_node and choosen node        
        ugraph[added_node] = choosen_nodes
        # Loops over choosen_node(s)
        for choosen_node in choosen_nodes:
            # Adds the edge to choosen nodes edge set
           ugraph[choosen_node].add(added_node)
    return ugraph 

###################################
# Code from Project-2
'''
Python code that implements breadth-first search. Then, uses this function to 
compute the set of connected components (CCs) of an undirected graph as well 
as determine the size of its largest connected component. Finally, a function 
that computes the resilience of a graph (measured by the size of its largest 
connected component) as a sequence of nodes are deleted from the graph.
'''  

def bfs_visited(ugraph, start_node):
    '''
    Takes the undirected graph ugraph and the node start_node and returns the 
    set consisting of all nodes that are visited by a breadth-first search 
    that starts at start_node.
    '''
    # Intialize an empty queue to store neighbors
    node_queue = deque()
    # Intialize a set to store visited node
    visited = set()
    # Add start_node to visited set
    visited.add(start_node)
    # Add start_node to node_queue
    node_queue.append(start_node)
    # Loops over non-empty node queue till empty
    while len(node_queue) > 0:
        # Removes a node from queue
        node = node_queue.popleft()
        # Loops over each neighbor of node
        for neighbor_node in ugraph[node]:
            # Checks if neighbor_node has been visited
            if neighbor_node not in visited:
                # Adds neighbor_node to visited
                visited.add(neighbor_node)
                # Adds neighbor_node to node_queue
                node_queue.append(neighbor_node)
    return visited
    
def cc_visited(ugraph):
    '''
    Takes the undirected graph ugraph and returns a list of sets, where each 
    set consists of all the nodes (and nothing else) in a connected component, 
    and there is exactly one set in the list for each connected component in 
    ugraph and nothing else.
    '''
    # Intializes a list of all nodes in ugraph
    remaining_nodes = ugraph.keys()
    # Intilaizes an empty list to store connected components (the output)
    connected_componets = list()
    # Loops over remaining_nodes till empty
    while len(remaining_nodes) > 0:
        # Gets first node in remaining_nodes
        node = remaining_nodes.pop(0)
        # Gets all the nodes connected to node in ugraph
        visited = bfs_visited(ugraph, node)
        # Saves the visited nodes (a connected component) to output
        connected_componets.append(visited)
        # Gets the nodes that are not part of visited 
        remaining_nodes = list(set(remaining_nodes) - visited)
    return connected_componets

def largest_cc_size(ugraph):
    '''
    Takes the undirected graph ugraph and returns the size (an integer) of 
    the largest connected component in ugraph.
    '''
    # Gets all the connected components in ugraph
    connected_componets = cc_visited(ugraph)
    # Initializes the known largest component seen to 0
    largest_component_size = 0
    # Loops over connected_components
    for component in connected_componets:
        # Checks if component is larger than largest component seen
        if len(component) > largest_component_size:
            # Sets the size of component to largest component seen
            largest_component_size = len(component)
    return largest_component_size

def compute_resilience(ugraph, attack_order):
    '''
    Takes the undirected graph ugraph, a list of nodes attack_order and 
    iterates through the nodes in attack_order. For each node in the list, the 
    function removes the given node and its edges from the graph and then 
    computes the size of the largest connected component for the resulting 
    graph. The function returns a list whose k+1th entry is the size of 
    the largest connected component in the graph after the removal of the 
    first k nodes in attack_order. The first entry (indexed by zero) is the 
    size of the largest connected component in the original graph.
    '''
    # Initializes a list to store output
    largest_connected_components = list()
    # Calculates and stores largest connected component of original graph
    largest_connected_components.append(largest_cc_size(ugraph))
    # Makes a copy of ugraph 
    attacked_graph = ugraph.copy()
    # Loops over nodes in attack_order
    for removed_node in attack_order:
        # Removes removed_node from attacked_graph
        attacked_graph.pop(removed_node, None)
        # Loops over all remaining nodes in attacked_graph
        for remaining_node in attacked_graph.keys():
            # Removes edges to removed_node in remaining nodes
            attacked_graph[remaining_node] = attacked_graph[remaining_node] - set([removed_node])
        # Calculates and stores largest connected component of original graph
        largest_connected_components.append(largest_cc_size(attacked_graph))
    return largest_connected_components

###################################
# Question 1
    
def calculate_edges_probability(ugraph):
    '''
    For undirect graph ugraph, calculates the probability used to generated 
    a graph with similar number of edges with Algorithm ER. Returns the 
    probability as a float.
    '''
    # Gathers all the in-degree values in a list
    path_list = [path for path_set in ugraph.values() for path in path_set]
    # Calculates the total number of edges in ugraph
    num_edges = float(len(path_list))
    # Calculates the total number of nodes
    num_nodes = float(len(ugraph))
    # Calculates the avergae number edges per node
    avg_edges = num_edges/num_nodes
    # Calculates probility using p = avg_edges/(num_nodes - 1)
    prob = avg_edges/(num_nodes - 1)
    return prob

def calulate_avg_degree(ugraph):
    '''
    For undirect graph ugraph, returns the average degree (number of edges) as
    a (a float).
    '''
    # Gathers all the in-degree values in a list
    path_list = [path for path_set in ugraph.values() for path in path_set]
    # Calculates the total number of edges in ugraph
    num_edges = float(len(path_list))
    # Calculates the total number of nodes
    num_nodes = float(len(ugraph))
    # Calculates the avergae number edges per node
    return num_edges/num_nodes

def random_order(graph):
    '''
    Returns a list of the nodes in graph in a random order.
    '''
    # Gets all the nodes in graph
    rand_node_list = graph.keys()
    # Randomly shuffles the nodes
    random.shuffle(rand_node_list)
    return rand_node_list

def get_graphs():
    '''
    Loads the computer network graphs and generates the simulated ER and UPA
    graphs. Returns these graphs in a list.
    '''
    # Loads the computer network graph
    computer_network_graph = load_graph(NETWORK_URL)    
    # Simulates the computer network graph with the algorithm ER
    simulated_ER_ugraph = algorithm_ER(len(computer_network_graph), 
                                       calculate_edges_probability(
                                               computer_network_graph))    
    # Simulates the computer network graph with the algorithm ER
    simulated_UPA_ugraph = algorithm_UPA(len(computer_network_graph.keys()), 
                                         int(math.ceil(calulate_avg_degree(computer_network_graph))))
    return [computer_network_graph, simulated_ER_ugraph, simulated_UPA_ugraph]

def attack_graphs(graph_list):
    '''
    Attacks the graphs in graphs list. Returns a pd dataframe with the 
    resilience of the graphs
    '''
    # Names of graphs
    row_names = ['computer_network_graph', 'simulated_ER_ugraph', 'simulated_UPA_ugraph']
    # Variable for indexing rows
    count = 0
    # Creates blank dataframe for storing results
    resilience_df = pd.DataFrame(index=np.arange(1, len(graph_list[0].keys())+1))
    ## Loops over graphs
    for graph in graph_list:
        print 'Attacking', row_names[count]
        # Generates attack order list
        attack_order = random_order(graph)
        # Attacks graph
        resilience_df[row_names[count]] = pd.Series(compute_resilience(graph, attack_order))
        # Increase index variable
        count += 1
    return resilience_df

def plot_Q1(resilience_df):
    '''
    Makes plot for Question 1
    '''
    # Choose dark colors
    sns.set_style("dark")   
    # plot the graph
    ax = resilience_df.plot(legend='best')
    # Add legend
    ax.legend(['Computer Network', 'Simulated ER (p=0.0040)', 'Simulated UPA (m=3)'])
    # Removes spines
    sns.despine()
    # Labels graph
    plt.title('Resilience of Three Graphs Under Continuous Attack.')
    plt.ylabel('Size of the largest connected component.')
    plt.xlabel('Number of nodes removed.')
    ax.grid(True)
    
def answer_Q1():
    ''' 
    Answers Q1.
    '''
    # Loads and simulates graphs
    graph_list = get_graphs()
    # Attacks graphs
    resilience_df = attack_graphs(graph_list)
    # Plots results
    plot_Q1(resilience_df)
    
#answer_Q1()    
    
###################################
# Question 2    

def answer_Q2():
    '''
    Answers Q2.
    '''
    print 'All three graphs are resilient under attack.'

#answer_Q2()     

###################################
# Question 3
    
def fast_targeted_order(ugraph):    
    """
    Compute a fast targeted attack order consisting of nodes of maximal degree.
    Returns: A list of nodes.
    """
    # Makes a copy of ugraph
    ugraph_copy = copy_graph(ugraph)
    # Initializes a dict for storing nodes with same degree
    degree_sets = dict()
    # Sets all the values in degree_sets to be empty
    for degree in range(len(ugraph.keys())):
        degree_sets[degree] = set([])
    # Loops over nodes in ugraph
    for node in ugraph.keys():
        # Calculates the degree node
        degree = len(ugraph[node])
        # Adds node to its place in degree_sets
        degree_sets[degree].add(node)
    # Initializes an empty list for storing output
    order_list = []
    # Loops over node degrees in reverse order
    for degree in range(len(ugraph_copy)-1, -1, -1):
        # Loops over degree_sets until empty
        while len(degree_sets[degree]) > 0:
            # Chooses a random node with degree 
            choosen_node = random.choice(list(degree_sets[degree]))
            # Removes choosen_node from degree_sets
            degree_sets[degree].remove(choosen_node)
            # Loops over each neighbor of choosen_node
            for neighbor in ugraph_copy[choosen_node]:
                # Calculates degree of neighbor node
                neighbor_degree = len(ugraph_copy[neighbor])
                # Removes neighor_degree from current degree_sets
                degree_sets[neighbor_degree].remove(neighbor)
                # Places neighbor_degree in degree_sets with one less degree
                degree_sets[neighbor_degree-1].add(neighbor)
            # Adds choosen_node to output            
            order_list.append(choosen_node)
            # Removes choosen node from graph
            delete_node(ugraph_copy, choosen_node)
    return order_list    
 
def test_fast_graphs():
    '''
    Generates the simulated UPA graphs under different node sizes and 
    calculates the time to run the functions target_order and 
    fast_target_order on them. Returns a pd dataframe with the results.
    '''
    # Disables garbage collection
    gc.disable()
    # Initializes dataframe for storing time (the output)
    running_time_df = pd.DataFrame(index=np.arange(10, 1000, 10), columns=['regular', 'fast'])
    # Initlializes variables for record keeping
    row_count = 0
    # Loops over different node sizes
    for num_nodes in range(10, 1000, 10):
        # Initlializes variables for record keeping
        column_count = 0
        # Simulates the computer network graph with the algorithm UPA
        simulated_graph = algorithm_UPA(num_nodes, 5)
        # Loops over target order functions
        for function in [targeted_order, fast_targeted_order]:
            # Gets current time in seconds
            start_time = time.clock() 
            # Performs target_order
            output = function(simulated_graph)
            # Calculates elapsed time
            elapsed_time = time.clock() - start_time
            # save elapsed time to dataframe
            running_time_df.iloc[row_count, column_count] = elapsed_time
            # Record keeping
            column_count += 1
        # Record keeping
        row_count += 1
    # Enables garbage collection    
    gc.enable()    
    return running_time_df

def plot_Q3():
    '''
    Makes the plot for answering Q3.
    '''
    running_time_df = test_fast_graphs()
    sns.set_style("dark")
    ax = running_time_df.plot(legend='best')
    ax.legend(['Regular', 'Fast'])
    # Removes spines
    sns.despine()
    ax.grid(True)
    # Labels graph
    plt.title('Running Time of Target Algorithms as a Function of Number of Nodes. \n (Performed on Desktop)')
    plt.ylabel('Running Time (in Seconds).')
    plt.xlabel('Size of UPA Graph, m = 5')
    
###################################
# Question 4   
    
def ordered_attack_graphs(graph_list):
    '''
    Uses ordered attacks on the graphs in graphs list. Returns a pd dataframe with the 
    resilience of the graphs
    '''
    # Names of graphs
    row_names = ['computer_network_graph', 'simulated_ER_ugraph', 'simulated_UPA_ugraph']
    # Variable for indexing rows
    count = 0
    # Creates blank dataframe for storing results
    resilience_df = pd.DataFrame(index=np.arange(1, len(graph_list[0].keys())+1))
    ## Loops over graphs
    for graph in graph_list:
        print 'Attacking', row_names[count]
        # Generates attack order list
        attack_order = fast_targeted_order(graph)
        # Attacks graph
        resilience_df[row_names[count]] = pd.Series(compute_resilience(graph, attack_order))
        # Increase index variable
        count += 1
    return resilience_df

def plot_Q4():
    '''
    Makes plot for Question 4
    '''
    graph_list = get_graphs()
    resilience_df = ordered_attack_graphs(graph_list)    
    # Choose dark colors
    sns.set_style("dark")   
    # plot the graph
    ax = resilience_df.plot(legend='best')
    # Add legend
    ax.legend(['Computer Network', 'Simulated UPA (m=3)', 'Simulated ER (p=0.0040)'])
    # Removes spines
    sns.despine()
    ax.grid(True)
    # Labels graph
    plt.title('Resilience of Three Graphs Under Ordered Attack.')
    plt.ylabel('Size of the largest connected component.')
    plt.xlabel('Number of nodes removed.')
        