"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# http://www.codeskulptor.org/#user43_GfFE4iKoMD_13.py

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)


def gen_sorted_sequences(outcomes, length):
    """
    Function that creates all sorted sequences via gen_all_sequences
    """    
    
    all_sequences = gen_all_sequences(outcomes, length)
    sorted_sequences = [tuple(sorted(sequence)) for sequence in all_sequences]
    
    return set(sorted_sequences)


def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    
    item_count = [item*hand.count(item) for item in set(hand)]
    
    return max(item_count)


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    
    new_rolls = gen_all_sequences(range(1, num_die_sides+1), num_free_dice) 
    scores = [score(roll + tuple(held_dice)) for roll in new_rolls]
    
    return sum(scores)/float(len(scores))
    


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
     
    choices = set()

    for temp in range(1,len(hand)+1):    
        choices = choices.union(gen_sorted_sequences(range(len(hand)), temp))

    sequences = set()
    for choice in choices:
        temp = set()
        for idx in choice:
            temp.add(idx)
        sequences.add(tuple(temp))

    pos_choices = set() 
    for sequence in sequences:
        dummy_choice = list()
        for die in sequence:
            dummy_choice.append(hand[die])
        pos_choices.add(tuple(dummy_choice))
    pos_choices.add(())
    
    return pos_choices


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    
    holds = gen_all_holds(hand)

    best_ev = 0
    for hold in holds:
        expect_value = expected_value(hold, num_die_sides, len(hand)-len(hold))
        if best_ev < expect_value:
            best_ev = expect_value
            best_hold = hold
    
    return (best_ev, best_hold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()

#print expected_value((1, 1, 1, 1, 1), 6, 1)

#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)      
        
