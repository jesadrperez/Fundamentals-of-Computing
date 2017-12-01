"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    if len(list1) <= 1:
        return list1
    else:
        unique_list = []    
        for num_elem in range(len(list1)-1):
            if list1[num_elem] < list1[num_elem+1]:
                unique_list.append(list1[num_elem])
        unique_list.append(list1[-1])              
                
    return unique_list       


def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    if (list1 == []) or (list2 == []):
        return []    
    inter_list = []
    for elem1 in list1:
        for elem2 in list2:
            if elem1 == elem2:
                inter_list.append(elem1)    
    
    return inter_list

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """   
    merge_list = list2[:]
    
    for elem in list1:
        for num in range(len(merge_list)):
            if elem <= merge_list[num]:
                merge_list.insert(num, elem)
                break
            elif num == len(merge_list)-1:
                merge_list.append(elem)
                break
                
    return merge_list
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    import math
    
    if len(list1) == 0:
        return []
    # base case
    elif len(list1) == 1:
        return list1
    elif len(list1) == 2:
        if list1[0] > list1[1]:
            return [list1[1], list1[0]]
        else:
            return list1    
    # recursive case
    else:
        split_list1 = list1[:int(math.ceil(len(list1)/2.0))]
        split_list2 = list1[int(math.ceil(len(list1)/2.0)):]        
        return merge(merge_sort(split_list1), merge_sort(split_list2))

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    # Base Case: 
    # Base Case: 
    if word == '':
        return ['']
    # Recursive Case
    else:
        single_letter = word[0]
        remaining_letters = word[1:]
        
        #print 'single_letter:', single_letter
        #print 'remaining_letters:', remaining_letters
        
        new_words = []   
        remaining_new_words = gen_all_strings(remaining_letters)
        #print 'remaining_new_words:', remaining_new_words
        
        # no insertion
        for word in remaining_new_words:
            #print '  word:', word
            new_words.append(word)           

        # insertion       
        for word in remaining_new_words:
            if len(word) == 0:
                new_words.append(single_letter)
            elif len(word) == 1:
                new_words.append(single_letter+word)
                new_words.append(word+single_letter)            
            else:
                new_words.append(single_letter+word)
                new_words.append(word+single_letter)
                
                for index in range(1, len(word)):
                    #print 'try:', word[0:index]+single_letter+word[index:] 
                    new_words.append(word[0:index]+single_letter+word[index:])
        return new_words 

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    return []

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
# run()

    
    