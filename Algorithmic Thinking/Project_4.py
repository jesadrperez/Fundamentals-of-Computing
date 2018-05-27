# -*- coding: utf-8 -*-
"""
Created on Thu May 24 07:22:28 2018

@author: Adrian
"""

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    '''
    Takes as input a set of characters and three scores and returns a dict of dict
    whose entries are indexed by pairs of characters in alphabet plus '-'.
    
    Inputs:
        alphabet - a set of characters
        dash_score - an interger score for any entry indexed by one or more dashes
        diag_score - an interger score for the remaining diagonial entries
        off_diag_score - an interger score for the remaining off_diagonal entries
    
    Output:
        scoring_matrix - a dictonary of dictonary whose entries are keyed by 
        pairs of characters in alphabet plus '-' and its value is the score for
        that pair.
    '''
    # init dict for storing results
    scoring_matrix = dict([])
    # Makes a copy of alphabet
    alphabet_copy = alphabet.copy()    
    # Adds dash to alphabet
    alphabet_copy.add('-')
    # Loop over each characters in alphabet
    for row_char in alphabet_copy:
        # Init a dict for each char 
        scoring_matrix[row_char] = dict([])
        # Loop over each char in alphabet
        for col_char in alphabet_copy:
            # Row_char or col_char is a '-':
            if (row_char == '-') or (col_char == '-'):
                # Assign dash_score
                scoring_matrix[row_char][col_char] = dash_score
            # row_char and col_char are not '-'
            else:
                # row_char and col_char are the same character
                if row_char == col_char:
                    # Assign diag_score
                    scoring_matrix[row_char][col_char] = diag_score
                # row_char and col_char are NOT the same character
                else:
                    scoring_matrix[row_char][col_char] = off_diag_score    
    return scoring_matrix    


def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    '''
    Computes the alignment matrix for two sequences using the method described
    in questions 8 or 12. 
    
    Inputs:
        seq_x, seq_y - two sequences whose elements share a common alphabet
        scoring_matrix - a dictonary of dictonary whose entries are keyed by 
        pairs of characters in alphabet plus '-' and its value is the score for
        that pair.
        global_flag - a binary value that when True computation is done using 
        the method in question 8, when False computation is done using the
        method in question 12.
    Output: alignment_matrix - a list of list
    '''
    # Compute the length of the sequences
    len_x = len(seq_x)
    len_y = len(seq_y)
    # Init list for storing output
    alignment_matrix = []
    # add all zeros to alignment matrix
    for dummy_row in range(len_x + 1):
        row_list = []
        for dummy_col in range(len_y + 1):
            row_list.append(0)
        alignment_matrix.append(row_list)     
    # Loop over the range of seq_x
    for dummy_row in range(1, len_x + 1):
        # calculate the score of this alignment
        alignment_value = alignment_matrix[dummy_row - 1][0] + scoring_matrix[seq_x[dummy_row - 1]]['-']
        # Use Q8 method
        if global_flag:
            # whatever this does
            alignment_matrix[dummy_row][0] = alignment_value 
        # Use Q12 Method
        elif alignment_value > 0:
            alignment_matrix[dummy_row][0] = alignment_value            
    # loop over the range of seq_y
    for dummy_col in range(1, len_y + 1):
        # calculate the score of this alignment
        alignment_value = alignment_matrix[0][dummy_col - 1] + scoring_matrix['-'][seq_y[dummy_col - 1]]
        # Use Q8 method
        if global_flag:
            # whatever this does
            alignment_matrix[0][dummy_col] = alignment_value
        # Use Q12 Method
        elif alignment_value > 0:
            alignment_matrix[0][dummy_col] = alignment_value
    # loop over every index in alignment_matrix
    for dummy_row in range(1, len_x + 1):
        for dummy_col in range(1, len_y + 1):
            value_1 = alignment_matrix[dummy_row-1][dummy_col-1]+scoring_matrix[seq_x[dummy_row - 1]][seq_y[dummy_col - 1]]
            value_2 = alignment_matrix[dummy_row-1][dummy_col]+scoring_matrix[seq_x[dummy_row - 1]]['-']
            value_3 = alignment_matrix[dummy_row][dummy_col-1]+scoring_matrix['-'][seq_y[dummy_col - 1]]
            if global_flag:
                # Assign the best of the three values
                alignment_matrix[dummy_row][dummy_col] = max(value_1, value_2, value_3)
            else:
                # Assign the best of the three values and 0
                alignment_matrix[dummy_row][dummy_col] = max(value_1, value_2, value_3, 0)
    return alignment_matrix  


def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    '''
    Takes two sequences whose elements share a common alphabet with the scoring
    matrix and computes the a global alignment of the two sequences using the
    global alignment matrix. Returns a tuple of the form score, alignment x, and 
    alignment y.
    Inputs:
        seq_x, seq_y - two sequences whose elements share a common alphabet
        scoring_matrix - a dictonary of dictonary whose entries are keyed by 
        pairs of characters in alphabet plus '-' and its value is the score for
        that pair.
        alignment_matrix - a list of list
    Output:
        score_tuple = a tuple of the form (score, alignment_x, alignment y)
    '''
    # Get the length of both sequences
    len_x = len(seq_x)
    len_y = len(seq_y)
    # Init alignments
    alignment_x = ''
    alignment_y = ''
    score = 0
    # Main loop
    while (len_x != 0) and (len_y != 0):
        if alignment_matrix[len_x][len_y] == alignment_matrix[len_x - 1][len_y - 1] + scoring_matrix[seq_x[len_x-1]][seq_y[len_y-1]]:
            alignment_x = seq_x[len_x-1] + alignment_x
            alignment_y = seq_y[len_y-1] + alignment_y
            len_x = len_x - 1
            len_y = len_y - 1
        else:
            if alignment_matrix[len_x][len_y] == alignment_matrix[len_x - 1][len_y] + scoring_matrix[seq_x[len_x-1]]['-']:
                alignment_x = seq_x[len_x-1] + alignment_x
                alignment_y = '-' + alignment_y
                len_x = len_x - 1
            else:
                alignment_x = '-' + alignment_x
                alignment_y = seq_y[len_y-1] + alignment_y
                len_y = len_y - 1            
    while (len_x != 0):
        alignment_x = seq_x[len_x-1] + alignment_x
        alignment_y = '-' + alignment_y
        len_x = len_x - 1
    while (len_y != 0):
        alignment_x = '-' + alignment_x
        alignment_y = seq_y[len_y-1] + alignment_y
        len_y = len_y - 1
        
    for index in range(len(alignment_x)):
        score += scoring_matrix[alignment_x[index]][alignment_y[index]]      
        
    return (score, alignment_x, alignment_y)

def compute_local_alignment(seq_x,seq_y,scoring_matrix,alignment_matrix):
    '''
    Takes two sequences whose elements share a common alphabet with the scoring
    matrix and computes the local alignment of the two sequences using the
    global alignment matrix. Returns a tuple of the form score, alignment x, and 
    alignment y.
    Inputs:
        seq_x, seq_y - two sequences whose elements share a common alphabet
        scoring_matrix - a dictonary of dictonary whose entries are keyed by 
        pairs of characters in alphabet plus '-' and its value is the score for
        that pair.
        alignment_matrix - a list of list
    Output:
        score_tuple = a tuple of the form (score, alignment_x, alignment y)
    '''
    # Init alignments and dash variable
    alignment_x = ''
    alignment_y = ''
    
    # Init variables to store 
    max_value = -1.0
    x_loc = -1
    y_loc = -1 
    
    # Find max value and its location (x_loc, y_loc) in the alignment matrix
    for index_i in range(len(alignment_matrix)):
        for index_j in range(len(alignment_matrix[0])):
            if max_value < alignment_matrix[index_i][index_j]:
                max_value = alignment_matrix[index_i][index_j]
                x_loc = index_i
                y_loc = index_j         

    # Main loop
    while (x_loc > 0) and (y_loc > 0):
        align_score = alignment_matrix[x_loc][y_loc]
        if align_score == alignment_matrix[x_loc - 1][y_loc - 1] + scoring_matrix[seq_x[x_loc - 1]][seq_y[y_loc - 1]]:
            alignment_x = seq_x[x_loc - 1] + alignment_x
            alignment_y = seq_y[y_loc - 1] + alignment_y
            x_loc = x_loc - 1
            y_loc = y_loc - 1    
        else:
            if align_score == alignment_matrix[x_loc - 1][y_loc] + scoring_matrix[seq_x[x_loc-1]]['-']:
                if align_score > 0:
                    alignment_x = seq_x[x_loc - 1] + alignment_x
                    alignment_y = '-' + alignment_y
                x_loc = x_loc - 1
            else:
                if align_score > 0:
                    alignment_x = '-' + alignment_x
                    alignment_y = seq_y[y_loc-1] + alignment_y
                y_loc = y_loc - 1
             
    return (max_value, alignment_x, alignment_y)