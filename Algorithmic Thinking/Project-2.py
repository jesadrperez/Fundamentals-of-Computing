# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 11:15:04 2018

@author: Adrian

Python code that implements breadth-first search. Then, uses this function to 
compute the set of connected components (CCs) of an undirected graph as well 
as determine the size of its largest connected component. Finally, a function 
that computes the resilience of a graph (measured by the size of its largest 
connected component) as a sequence of nodes are deleted from the graph.
"""

# Common Imports
from collections import deque

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