# -*- coding: utf-8 -*-
"""
Created on Thu May 24 21:40:18 2018

@author: Adrian
"""
import alg_application4_provided as provided
import Project_4 as student
import random
import pandas as pd
import seaborn as sns
import numpy as np
import string

sns.set_style("dark")

# URLs for data files
PAM50_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_PAM50.txt"
HUMAN_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_ConsensusPAXDomain.txt"
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"


###############################################
# Question 1

def answer_Q1():
    '''
    Answers Q1.
    '''
    # load the acid sequences that form the eyeless proteins for humans genomes
    human_sequence = provided.read_protein(HUMAN_EYELESS_URL)
    # load the acid sequences that form the eyeless proteins for fruit flies genomes
    fly_sequence = provided.read_protein(FRUITFLY_EYELESS_URL)
    # load the PAM50 scoring matrix
    pam50_scoring_matrix = provided.read_scoring_matrix(PAM50_URL)
    # compute the alignment method using method Q12
    alignment_matrix = student.compute_alignment_matrix(human_sequence, fly_sequence, pam50_scoring_matrix, False)
    return student.compute_local_alignment(human_sequence, fly_sequence, pam50_scoring_matrix, alignment_matrix)

###############################################
# Question 2

def percent_match(local_alignment):
    ''' 
    Computes the percent similarilty between a local alignment to the 
    global alignment of the PAX sequence.
    '''
    # remove the '-' from the local alignment
    local_alignment = local_alignment.replace('-', '')
    # load the PAM50 scoring matrix
    pam50_scoring_matrix = provided.read_scoring_matrix(PAM50_URL)
    # load the consensus sequence
    consensus_sequence = provided.read_protein(CONSENSUS_PAX_URL)
    # compute the global alignment
    alignment_matrix = student.compute_alignment_matrix(local_alignment, consensus_sequence, pam50_scoring_matrix, True)
    # compute the global alignment
    score, global_alignment, consensus_alignment = student.compute_global_alignment(local_alignment, consensus_sequence, pam50_scoring_matrix, alignment_matrix)
    # Init the variable to store matches
    match = 0
    # loop over each character
    for char in range(len(global_alignment)):
        # compare characters between the two alignments
        if global_alignment[char] == consensus_alignment[char]:
            # increase the match score by 1
            match += 1
    return round(match/float(len(global_alignment))*100, 2)

def answer_Q2():
    '''
    Answers Q2.
    '''
    # load the previous sequences    
    score, human_sequence, fly_sequence = answer_Q1()
    return (percent_match(human_sequence), percent_match(fly_sequence))

###############################################
# Question 3
    
###############################################
# Question 4
    
def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    '''
    blah, blah, blah.
    Input:
        seq_x, seq_y - two sequences that share a common alphabet
        scoring_matrix - 
        num_trials - 
    Output:
        scoring_distribution - a dict of scores, which the key is the score and value 
        is the number of times that score has appeared in the trials
    '''
    # Init dict to store scores
    scoring_distribution = dict()
    # Perform trails
    while sum(scoring_distribution.values()) < num_trials:
        # convert seq_y into a list
        list_y = list(seq_y)
        # generates a random permutation of the list of seq_y
        random.shuffle(list_y)
        # convert the list into a string
        rand_y = ''.join(list_y)
        # Compute the alignment matrix
        alignment_matrix = student.compute_alignment_matrix(seq_x, rand_y, scoring_matrix, False)
        # Score the local alignments
        score, align_x, align_y = student.compute_local_alignment(seq_x, rand_y, scoring_matrix, alignment_matrix)
        # Check if score is already in scoring_distribution
        if score in scoring_distribution.keys():
            # Increment the score by 1
            scoring_distribution[score] += 1
        else:
            # Add score and set value to 1
            scoring_distribution[score] = 1
    return scoring_distribution

def perform_human_fly_trials():
    # load the acid sequences that form the eyeless proteins for humans genomes
    human_sequence = provided.read_protein(HUMAN_EYELESS_URL)
    # load the acid sequences that form the eyeless proteins for fruit flies genomes
    fly_sequence = provided.read_protein(FRUITFLY_EYELESS_URL)
    # load the PAM50 scoring matrix
    pam50_scoring_matrix = provided.read_scoring_matrix(PAM50_URL)
    # perform 1000 trials
    scoring_distribution = generate_null_distribution(human_sequence, fly_sequence, pam50_scoring_matrix, 1000)
    # conver result to pd dataframe
    scoring_dist_df = pd.DataFrame(scoring_distribution.values(), index=scoring_distribution.keys(), columns=['Frequency'])
    # fix index name
    scoring_dist_df.index.rename('Scores', inplace=True)
    return scoring_dist_df

def answer_Q4(save):
    # load the data
    scoring_dist_df = perform_human_fly_trials()
    # compute the normalized frequency
    scoring_dist_df['Norm Freq'] = scoring_dist_df['Frequency']/scoring_dist_df['Frequency'].sum()
    # plot the data
    ax = scoring_dist_df['Norm Freq'].plot.bar(title='Null Distribution of 1000 Trials')
    # label the axes 
    ax.set(xlabel='Scores',  ylabel='Fraction of Trials')
    # add grid
    ax.grid(True)
    # Saves the plot
    if save:
        fig = ax.get_figure()
        fig.savefig('Application 4 - Q4.png')
        
        
###############################################
# Question 5     

def answer_Q5():
    # get the null dist data        
    scoring_dist_df = perform_human_fly_trials()
    # get the score from the local alignments
    score, human_sequence, fly_sequence = answer_Q1()
    # Init list to store scores    
    null_scores = []
    # loop over data frame
    for index, row in scoring_dist_df.iterrows():
        dummy_list = [int(index)]*row['Frequency']
        for element in dummy_list:
            null_scores.append(element)
    # calculate mean            
    mean = np.mean(null_scores)
    # calculate std
    std = np.std(null_scores)
    # calculate z-score
    z_score = (score - mean)/std
    return (mean, std, z_score)


###############################################
# Question 7

def answer_Q7():
    alphabet = set(['A', 'C', 'T', 'G'])
    diag_score = 2
    off_diag_score = 1
    dash_score = 0
    
    seq_x = 'AA' 
    seq_y = 'TAAT'
    
    scoring_matrix = student.build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score)
    alignment_matrix = student.compute_alignment_matrix(seq_x, seq_y, scoring_matrix, True)
    
    score, align_x, align_y = student.compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix)
    
    edit_distance = len(seq_x) + len(seq_y) - score
    
    return (diag_score, off_diag_score, dash_score)


###############################################
# Question 8
    
def check_spelling(checked_word, dist, word_list):
    '''
    Iterates through word_list and returns the set of all words that are within 
    edit distance dist of the string checked_word.
    '''
    # Set constants 
    ALPHABET = set(list(string.ascii_lowercase))
    DIAG_SCORE = 2
    OFF_DIAG_SCORE = 1
    DASH_SCORE = 0
    # contruct scoring matrix over all lower case letters
    scoring_matrix = student.build_scoring_matrix(ALPHABET, DIAG_SCORE, OFF_DIAG_SCORE, DASH_SCORE)
    # Init list to store words
    close_words = []
    # Loop over word in word_list
    for word in word_list:
        # compute alignment matrix
        alignment_matrix = student.compute_alignment_matrix(checked_word, word, scoring_matrix, True)
        # compute score of global alignments
        score, align_x, align_y = student.compute_global_alignment(checked_word, word, scoring_matrix, alignment_matrix)
        # calculate edit distance
        edit_distance = len(checked_word) + len(word) - score
        # Compare edit_distance and dist
        if edit_distance <= dist:
            # save word
            close_words.append(word)
    return close_words

def answer_Q8()    
    word_list = provided.read_words(WORD_LIST_URL)    
    return (check_spelling("humble", 1, word_list), check_spelling("firefly", 2, word_list)) 

    