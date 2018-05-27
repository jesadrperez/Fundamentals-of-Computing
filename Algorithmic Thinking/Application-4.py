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
    # make a copy of the local alignment
    alignment_copy = local_alignment[:]
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

def answer_Q4():
    # load the data
    scoring_dist_df = scoring_dist_df
    # compute the normalized frequency
    scoring_dist_df['Norm Freq'] = scoring_dist_df['Frequency']/scoring_dist_df['Frequency'].sum()
    # plot the data
    ax = scoring_dist_df['Norm Freq'].plot.bar(title='Null Distribution of 1000 Trials')
    # label the axes 
    ax.set(xlabel='Scores',  ylabel='Fraction of Trials')
    # add grid
    ax.grid(True)
    