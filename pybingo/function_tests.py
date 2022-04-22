from copy import deepcopy
from time import perf_counter_ns
def find_max_list_idx(numbers):
    import numpy as np
    from more_itertools import locate
    list_len = [len(i) for i in numbers]
    arr = np.array(list_len)
    response = np.argmax(arr)
    val = arr.max()
    return list(locate(arr, lambda x: x == val))

def assign_numbers(numbers, pre_selected=None):
    """Assign all the numbers required to a board. Pass in our remaining numbers


    Args:
        numbers (_type_): _description_
    """
    import random
    remaining_numbers = deepcopy(numbers)

    # take 1 or 2 values from each list totalling 15 values
    # Must take 1 value. May take 2 to get the total chosen to 15.
    # Must have 5 values on each row leaving 4 empty positions
    
    # Sort numbers
    need_count = 15
    selected = []
    for collection in remaining_numbers:
        # get first 9 positions.
        import random
        val = random.choice(collection)
        selected.append(val)
        collection.remove(val)
    # Pick 15 numbers
    # Between 1 and 90
    # 1 from each 1-9(ten value)
    # assign 6 more values to the board from a random selection of ten values
    # if there's one with more than the rest take from that ten list
    # otherwise select again randomly
    # randomise remaining 6
    # if theres 6 values definitely distributed leaves 4 each column to distribute evenly so 36 remaining numbers
    while len(selected) != need_count:  
        # if theres any indexes with more len than the rest choose their first
        more_than_the_rest = find_max_list_idx(remaining_numbers)
        print(more_than_the_rest)
        collection_index = random.sample(more_than_the_rest, 1)
        print(collection_index)
        
        val = random.choice(remaining_numbers[collection_index[0]])
        remaining_numbers[collection_index[0]].remove(val)
        selected.append(val)
    print(selected.sort())    
    return {'selected': selected, 'remaining': remaining_numbers}
    # Then sort positioning
    # 2 options
    '''
        1) Assign the spaces before filling with any numbers that way the space positioning appears more random
        2) 
    '''

def generate_modern(board_count=1):
    """Create a 1-90 bingo sheet. And assign a number of boards (Max 6) 
    """
    t1_start = perf_counter_ns()
    # generate our lists for each unit
    numbers = [] 
    for tens in range(9):
        dec = []
        for units in range(9): 
            dec.append(int(f'{tens}{units+1}'))
        dec.append(int(f'{tens+1}0'))
        numbers.append(dec)
    t1_stop = perf_counter_ns()

    print(numbers)
    board = assign_numbers(numbers)
    print(f'Elapsed time: {t1_stop} {t1_start}')
 
 
    print("Elapsed time during the whole program in nano seconds:",
                                        t1_stop-t1_start, 'ns')
    return board

generate_modern()

