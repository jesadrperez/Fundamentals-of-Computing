"""
Provided code for Application portion of Module 1

Imports physics citation graph 
"""

# general imports
import urllib2
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import random
import numpy as np

# Set timeout for CodeSkulptor if necessary
#import codeskulptor
#codeskulptor.set_timeout(20)


###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

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
# Helper functions
    
def make_complete_graph(num_nodes):
    '''
    Takes the number of nodes and returns a dictionary 
    corresponding to a complete directed graph with the 
    specified number of nodes. 
    '''    
    if num_nodes == []:
        return dict([])
    else:
        # creates empty dictonary for storing
        complete_graph = dict([])
        # generates the nodes
        node_list = range(num_nodes)
        # loops over nodes and generates path
        for node in node_list:
            # creates dummy node list used for paths
            dummy_node_list = node_list[:]
            # removes node from dummy_node_list
            dummy_node_list.remove(node)
            # saves paths to dict
            complete_graph[node] = set(dummy_node_list)
        return complete_graph

def compute_in_degrees(digraph):
    '''
    Takes a directed graph (represented as a dictionary) and computes the 
    in-degrees for the nodes in the graph. The function returns a dictionary 
    with the same set of keys (nodes) as whose corresponding values are the 
    number of edges whose head matches a particular node.
    '''
    # Gathers all paths into a single list
    path_list = [path for path_set in digraph.values() for path in path_set]   
    # Creates dict for storing in degrees by node
    in_degrees_dict = dict([])
    # Loops over nodes
    for node in digraph.keys():
        # Calculates the in degree of node
        in_degrees_dict[node] = path_list.count(node)
    return in_degrees_dict

def in_degree_distribution(digraph):
    '''
    Takes a directed graph (represented as a dictionary) and computes the 
    unnormalized distribution of the in-degrees of the graph. The function 
    returns a dictionary whose keys correspond to in-degrees of nodes in the 
    graph. The value associated with each particular in-degree is the number 
    of nodes with that in-degree. In-degrees with no corresponding nodes in 
    the graph are not included in the dictionary.
    '''
    # Computes the in-degree of each node     
    in_degrees_dict = compute_in_degrees(digraph)
    # Gathers all the in-degree values in a list
    in_degree_list = [in_degree for in_degree in in_degrees_dict.values()]
    # Finds all the unique in-degrees
    in_degrees = list(set(in_degree_list))
    # Creates dict for storing values
    in_degree_dist_dict = dict([])
    # Loops over in-degrees
    for in_degree in in_degrees:
        # Computes the distribution of in_degree
        in_degree_dist_dict[in_degree] = in_degree_list.count(in_degree)
    return in_degree_dist_dict   

def algorithm_ER(num_nodes, prob):
    '''
    Computes a random directed graph with num_nodes, where the likelihood that 
    two nodes (i,j) have a direct edge from i to j with probability prob.
    Returns a dict.
    '''
    # Creates an empty graph dict
    digraph = dict()
    # Adds all nodes to dict with no edges
    for node in range(num_nodes):
        digraph[node] = []    
    # Computes all pairwise permutations
    node_pairs = itertools.permutations(range(num_nodes), 2)
    # Loops over all pairwise permutations
    for node_i, node_j in node_pairs:
        # Calculates a random uniform value
        chance = random.uniform(0, 1)
        # Checks if chance is less than prob
        if chance < prob:
            # Adds a directed path from node_i to node_j
            digraph[node_i].append(node_j) 
    return digraph

class DPATrial:
    """
    Provided code for application portion of module 1

    Helper class for implementing efficient version
    of DPA algorithm
    
    Simple class to encapsulate optimized trials for DPA algorithm
    
    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a DPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors  

###################################
# Question 1

def normalize_digraph_distribution(digraph):
    '''    
    Calculates the normalized in-degree distribution of this graph.
    Returns a pd.series
    '''
    # Calculates the in-degree distribution
    in_degree_dist = in_degree_distribution(digraph)
    # Converts the in-degree dist to float and series
    in_degree_values = pd.Series(in_degree_dist).astype('float')
    # Normalizes the in-degree distribution
    in_degree_values_norm = in_degree_values/in_degree_values.sum()
    return in_degree_values_norm

def plot_citation_graph():
    '''
    Plot a log log plot of the normalized distribution in-degrees of the 
    citation graph.
    Returns nothing.
    '''
    # Load the citation graph    
    citation_graph = load_graph(CITATION_URL)
    # Compute the normalized distribution in-degree values
    in_degree_values_norm = normalize_digraph_distribution(citation_graph)
    # Creates loglog plot 
    plt.loglog(in_degree_values_norm, 'o')
    # Corrects x-axis
    plt.xlim(10**0, 10**3.4)
    # Corrects y-axis
    plt.ylim(10**-5, 10**0)
    # Adds main and sub grids
    plt.grid(True, which='both')
    # Adds title
    plt.title('LogLog Plot of the Normalized Distribution of the In-Degrees of a Citation Graph \n for 27,770 High Energy Physics Theory Papers.')
    # Adds x label
    plt.xlabel('Number of Citations')
    # Adds y label
    plt.ylabel('Fraction of Papers')
    
#plot_citation_graph()    

###################################
# Question 2

def make_random_ER_graph(num_nodes, prob):
    '''
    Makes a random digraph with num_nodes and the link probability p. 
    Returns a dictiionary.
    '''
    # Makes the random digraph
    return algorithm_ER(num_nodes, prob)  

#plt.loglog(make_in_degree_norm(27770, 0.001))
    
###################################
# Question 3
    
def calculate_avg_edges(digraph):
    '''
    Calculates the avarge number of edges per node in a digraph. 
    Returns an interger.
    '''
    # Gathers all the in-degree values in a list
    path_list = [path for path_set in digraph.values() for path in path_set]
    return len(path_list)/len(digraph)

NODE_CONNECTION = calculate_avg_edges(load_graph(CITATION_URL))
NUM_NODES = len(load_graph(CITATION_URL))
    
###################################
# Question 4
    
def algorithm_DPA(num_nodes, node_connection):
    '''
    Generates a synthetic directed graph with num_nodes. First a complete 
    directed graph is generated on node_connection nodes. Then, the graph is 
    grown by adding num_nodes - node_connection nodes. Where each new node is 
    connected to node_connection nodes randomly chosen from the set of existing
    nodes.
    Returns a dictionary of the digraph.
    '''
    # Makes a complete graph with node_connection nodes
    digraph = make_complete_graph(node_connection)
    # Loads provided class for chosing subset nodes
    node_chooser = DPATrial(node_connection)
    # Adds missing nodes (num_nodes - node_connection nodes)
    for added_node in range(node_connection, num_nodes):
        # Chooses node_connection subet of nodes
        digraph[added_node] = set(node_chooser.run_trial(node_connection))
    return digraph   
    
simulated_DPA_digraph = algorithm_DPA(NUM_NODES, NODE_CONNECTION)

# Corrects x-axis
plt.xlim(10**0, 10**4)
# Corrects x-axis
plt.ylim(10**-5, 10**0)
# Adds main and sub grids
plt.grid(True, which='both')
# Adds title
plt.title('LogLog Plot of Normalized In-Degree Distribution of a\n Simulated Graph Generated with the DPA Algorithm.')
# Adds x label
plt.xlabel('Number of Citations')
# Adds y label
plt.ylabel('Fraction of Papers')