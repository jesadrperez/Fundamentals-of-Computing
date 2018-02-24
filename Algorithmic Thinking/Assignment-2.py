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
    # Loops over non-empty node queue
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