"""
Provided code for Application portion of Module 1

Imports physics citation graph 
"""

# general imports
import urllib2
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
    # Computes the in_degree of each node     
    in_degrees_dict = compute_in_degrees(digraph)
    # Gathers all the in_degree values in a list
    in_degree_list = [in_degree for in_degree in in_degrees_dict.values()]
    # Finds all the unique in degrees
    in_degrees = list(set(in_degree_list))
    # Creates dict for storing values
    in_degree_dist_dict = dict([])
    # Loops over in degrees
    for in_degree in in_degrees:
        # Computes the distribution of in_degree
        in_degree_dist_dict[in_degree] = in_degree_list.count(in_degree)
    return in_degree_dist_dict   

###################################
# Question 1

# Load the citation graph    
citation_graph = load_graph(CITATION_URL)
# Compute the unnormalized distribution of the in-degrees of the graph
in_degree_dist_citation = in_degree_distribution(citation_graph)
# Convert the in-degrees to floats
in_degree_values = np.array(in_degree_dist_citation.values()).astype('float')
# Compute the normalized distribution in-degree values
in_degree_values_norm = in_degree_values/np.sum(in_degree_values)

plt.loglog(in_degree_dist_citation.keys(), in_degree_values_norm)
