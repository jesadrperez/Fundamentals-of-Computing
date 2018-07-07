# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 15:42:26 2018

@author: Adrian
"""

import itertools

######################################################
# Question 2

var1 = 7

def var0(var1, var2):
    var3 = var1 + var2
    global var4
    var4 = 17
    return var3 + var4
    
#print var0(var1, var1)


######################################################
# Question 5

class BankAccount:
    def __init__(self, initial_balance):
        """
        Creates an account with the given balance.
        """
        self.balance = initial_balance
        self.fees = 0

    def deposit(self, amount):
        """
        Deposits the amount into the account.
        """
        self.balance = self.balance + amount

    def withdraw(self, amount):
        """
        Withdraws the amount from the account.  
        Each withdrawal resulting in a balance of 
        less than 10 dollars (before any fees) also 
        deducts a penalty fee of 5 dollars from the balance.
        """
        self.balance = self.balance - amount
        if self.balance < 10:
            self.balance = self.balance - 5
            self.fees = self.fees + 5

    def get_balance(self):
        """
        Returns the current balance in the account.
        """
        return self.balance

    def get_fees(self):
        """
        Returns the total fees ever deducted from the account.
        """
        return self.fees
    
account1 = BankAccount(20)
account1.deposit(10)
account2 = BankAccount(10)
account2.deposit(10)
account2.withdraw(50)
account1.withdraw(15)
account1.withdraw(10)
account2.deposit(30)
account2.withdraw(15)
account1.deposit(5)
account1.withdraw(20)
account2.withdraw(15)
account2.deposit(25)
account2.withdraw(15)
account1.deposit(10)
account1.withdraw(50)
account2.deposit(25)
account2.deposit(25)
account1.deposit(30)
account2.deposit(10)
account1.withdraw(15)
account2.withdraw(10)
account1.withdraw(10)
account2.deposit(15)
account2.deposit(10)
account2.withdraw(15)
account1.deposit(15)
account1.withdraw(20)
account2.withdraw(10)
account2.deposit(5)
account2.withdraw(10)
account1.deposit(10)
account1.deposit(20)
account2.withdraw(10)
account2.deposit(5)
account1.withdraw(15)
account1.withdraw(20)
account1.deposit(5)
account2.deposit(10)
account2.deposit(15)
account2.deposit(20)
account1.withdraw(15)
account2.deposit(10)
account1.deposit(25)
account1.deposit(15)
account1.deposit(10)
account1.withdraw(10)
account1.deposit(10)
account2.deposit(20)
account2.withdraw(15)
account1.withdraw(20)
account1.deposit(5)
account1.deposit(10)
account2.withdraw(20)
#print account1.get_balance(), account1.get_fees(), account2.get_balance(), account2.get_fees()   

######################################################
# Question 10

class Stack:
    def __init__(self, items):
        self.items = items
        
    def __str__(self):
        return self.items

    def Add(self, item):
        self.items.append(item)
        
    def Rem(self):
        self.items.pop()
        
stack = Stack([])
stack.Add(4)
stack.Add(8)
stack.Rem()
stack.Add(7)
stack.Add(6)
stack.Add(5)
stack.Rem()
stack.Rem()
stack.Add(2)
stack.Rem()
stack.Add(3)
stack.Add(7)            
#  print stack.items

######################################################
# Question 12

def probability(outcomes):
    
    prob_dict = {1:0.10, 2:0.20, 3:0.30, 4:0.150, 5:0.050, 6:0.20}
    
    if len(outcomes) == 1:
        return prob_dict[outcomes[0]]
    else:
        return prob_dict[outcomes[0]] * probability(outcomes[1:])

#probability([4, 2, 6, 4, 2, 4, 5, 5, 5, 5, 1, 2, 6, 2, 6, 6, 4, 6, 2, 3, 5, 5, 2, 1, 5, 5, 3, 2, 1, 4, 4, 1, 6, 6, 4, 6, 2, 4, 3, 2, 5, 1, 3, 5, 4, 1, 2, 3, 6, 1])

######################################################
# Question 17

def pick_a_number(board):
    result = [0, 0]
    player_one = True

    while len(board) > 0:
        if board[0] > board[-1]:
            best_value = board.pop(0)
        else:
            best_value = board.pop(-1)
        if player_one:
            result[0] = result[0] + best_value
        else:
            result[1] = result[1] + best_value
        player_one = not player_one    
    return result

pick_a_number([12, 9, 7, 3, 4, 7, 4, 3, 16, 4, 8, 12, 1, 2, 7, 11, 6, 3, 9, 7, 1])
            
######################################################
# Question 21

GRAPH21 = {1 : set([]), 2 : set([3,7]), 3 : set([2,4]), 4 : set([3, 5]), 5 : set([4, 6]), 6 : set([5, 7]), 7 : set([2, 6])}


######################################################
# Question 25

def make_subset_graph(subset_nodes, graph):
    '''
    Makes a subset graph of graph that includes only the nodes in subset_nodes.
    Outputs this new graph as a dict.
    '''
    # Init graph
    subset_graph = {}
    # Find removed nodes (nodes in org graph but not in subset)
    removed_nodes = set(graph.keys()) - set(subset_nodes)
    # Loop over subset_nodes
    for node in subset_nodes:
        # Add node to subset graph and edges involving only subset nodes
        subset_graph[node] = graph[node] - removed_nodes
    return subset_graph

def get_all_egdes(graph):
    '''
    Makes a list of tuples of all the connections (edges) in the graph.
    '''
    connections = [] 
    for node in graph.keys():
        for edge in graph[node]:
            connections.append((node, edge))
    return connections
            
def mystery(graph):
    n = len(graph)
    for i in range(n + 1):
        for subset_nodes in itertools.combinations(graph.keys(), i):
            subset_graph = make_subset_graph(list(subset_nodes), graph)
            flag = True        
            conn = get_all_egdes(graph)
            sub_conn = get_all_egdes(subset_graph)            
            for edge in conn:
                print edge
                if edge not in sub_conn:
                    flag = False
                    break
            if flag:
                return subset_graph