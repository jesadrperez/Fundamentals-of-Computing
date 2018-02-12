'''
Python code that creates dictionaries corresponding to 
some simple examples of graphs. Implement two short 
functions that compute information about the distribution 
of the in-degrees for nodes in these graphs.
'''

# Representing Directed Graphs

EX_GRAPH0 = {0:set([1,2]), 
             1:set([]), 
             2:set([])
            }
EX_GRAPH1 = {0:set([1,4,5]),
             1:set([2,6]),
             2:set([3]),
             3:set([0]),
             4:set([1]),
             5:set([2]),
             6:set([])
            }
EX_GRAPH2 = {0:set([1,4,5]),
             1:set([2,6]),
             2:set([3,7]),
             3:set([7]),
             4:set([1]),
             5:set([2]),
             6:set([]),
             7:set([3]),
             8:set([1,2]),
             9:set([0,3,4,5,6,7])
            }
             
#print 'EX_GRAPH0', EX_GRAPH0
#print 'EX_GRAPH1', EX_GRAPH1
#print 'EX_GRAPH2', EX_GRAPH2

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
    
# Computing degree distributions

def compute_in_degrees(digraph):
    '''
    Takes a directed graph (represented as a dictionary) 
    and computes the in-degrees for the nodes in the 
    graph. The function returns a dictionary with 
    the same set of keys (nodes) as whose corresponding 
    values are the number of edges whose head matches a 
    particular node.
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
