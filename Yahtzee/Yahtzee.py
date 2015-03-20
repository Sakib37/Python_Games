#http://www.codeskulptor.org/#user39_0VBEZ7urdC_4.py

# http://www.codeskulptor.org/#user39_0VBEZ7urdC_8.py

#http://www.codeskulptor.org/#user39_0VBEZ7urdC_10.py

# http://www.codeskulptor.org/#user39_yF6pzBXJRXAEWZ8.py

"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

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
    hand_score = 0
    new_score = 0
    for item in hand:
        new_score = hand.count(item) * item
        if new_score > hand_score:
            hand_score = new_score
    return hand_score


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    all_seq_free_dice = gen_all_sequences(range(1, (num_die_sides + 1)), num_free_dice)
    possible_score = 0
    for seq in all_seq_free_dice:
        score_arg = tuple(sorted(list(held_dice) + list(seq)))
        possible_score += score(score_arg)
    return possible_score / float(num_die_sides ** num_free_dice)


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    holds = set([])
    hand_length = len(hand)
    binary_counts =[bin(x)[2:].rjust(hand_length,'0') for x in range(2**hand_length)]
    print binary_counts
    for item in binary_counts:
        tmp = []
        count = 0
        for bit in item:
            if int(bit) == 1:
                tmp.append(hand[count])
            count += 1
        holds.add(tuple(tmp))
    return holds


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    max_expected = 0.0
    for seq in gen_all_holds(hand):
        if expected_value(seq, num_die_sides, (len(hand) - len(seq))) > max_expected:
            max_expected = expected_value(seq, num_die_sides, (len(hand) - len(seq)))
            dice_choice = seq        
    return (max_expected, dice_choice)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
#run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    




