B_col = 0
I_col = 1
N_col = 2
G_col = 3
O_col = 4
B = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
I = [16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
N = [31,32,33,34,35,36,37,38,39,40,41,42,43,44,45]
G = [46,47,48,49,50,51,52,53,54,55,56,57,58,59,60]
O = [61,62,63,64,65,66,67,68,69,70,71,72,73,74,75]

from timeit import default_timer as timer
from unittest import case
import numpy as np


config = {
        # Modes are classic (BINGO 1-75) and modern (9x3 1-90)
        'mode': 'classic',
        'win_by_row': False,
        'win_by_column':False,
        'win_by_diagonal':False,
        'win_by_corners':False,
        'win_by_all':True
    }
class Board(object):
    _numbers_as_list = []
    _numbers = []
    def __init__(self):
        self._numbers = self.generate(config['mode'])
        all = []
        for val in self._numbers:
            all = list(set(all + val))
        self._numbers_as_list = all
        print(all)
    def to_td(self, numbers_as_bingo):
        td_numbers = []

        # for column in numbers_as_bingo:
        for i in range(len(numbers_as_bingo)):
            td_numbers.append([x[i] for x in numbers_as_bingo])

        return td_numbers
    def generate(self, mode):
        if mode == 'classic':
            import random
            from copy import deepcopy
            _b = deepcopy(B)
            _i = deepcopy(I)
            _n = deepcopy(N)
            _g = deepcopy(G)
            _o = deepcopy(O)

            #pick 5 from each but N pick 4
            b_choices = []
            i_choices = []
            n_choices = []
            g_choices = []
            o_choices = []

            for i in range(5):

                if i != 4:
                    n_val = random.choice(_n)
                    n_choices.append(n_val)
                    _n.remove(n_val) 

                b_val = random.choice(_b)
                b_choices.append(b_val)
                _b.remove(b_val)

                i_val = random.choice(_i)
                i_choices.append(i_val)
                _i.remove(i_val)

                g_val = random.choice(_g)
                g_choices.append(g_val)
                _g.remove(g_val)

                o_val = random.choice(_o)
                o_choices.append(o_val)
                _o.remove(o_val)


            b_choices.sort()
            i_choices.sort()
            n_choices.sort()
            # assign the free space to the center
            n_choices.insert(2, 0)

            g_choices.sort()
            o_choices.sort()
            nums_as_td_array = self.to_td([b_choices, i_choices, n_choices, g_choices, o_choices])
        else:
            # modern 3x9 1-90
            # 9 arrays of 1-10
            # generate our lists for each unit
            all_numbers = [] 
            for tens in range(9):
                dec = []
                for units in range(9): 
                    dec.append(int(f'{tens}{units+1}'))
                dec.append(int(f'{tens+1}0'))
                all_numbers.append(dec)
            
            
            # now we need to grab 1-3 values from each 
        return nums_as_td_array

    def set_numbers(self, numbers):
        if isinstance(numbers, list):
            self._numbers = numbers
            return True
        else:
            return False
    def mark_as_called(self, col, row):
        if self._numbers[row][col]== 0:
            return 'X' 
        else:
            return self._numbers[row][col] 
    def print_numbers(self):
        if self._numbers != {}:
            print('B - I - N - G - O')
            for i in range(5):
                print(f"{self.mark_as_called(B_col, i)} {self.mark_as_called(I_col, i)} {self.mark_as_called(N_col,i)} {self.mark_as_called(G_col, i)} {self.mark_as_called(O_col, i)}")
        else:
            print('No Numbers generated')
    def mark_number(self, val):
        if val in self._numbers_as_list:
            for i in range(5):
                if val in self._numbers[i]:
                    index = self._numbers[i].index(val)
                    self._numbers[i][index] = 0
                    # self.print_numbers()
                    return True
        return False
    def check_bingo(self):
        if config['win_by_row']:
            for i in range(5):
                if len(set(list(self._numbers[i]))) == 1:
                    return True

        if config['win_by_column']:
            for i in range(5):
                lst = [item[i] for item in self._numbers]
                if len(set(lst)) == 1:
                    return True

        if config['win_by_diagonal']:
            # check two diagonal possibilities
            # need [(0,0), (1,1),(2,2),(3,3),(4,4)] & [(0,4), (1,3), (2,2), (3,1) ,(4,0) ]
            lsta = []
            lstb = []
            max = len(self._numbers[0])
            for i in range(max):
                x = i
                y = max-(x+1)
                lsta.append(self._numbers[x][x])
                lstb.append(self._numbers[x][y])
                # = [item[y] for item in self._numbers]
            if len(set(lsta)) == 1 or len(set(lstb)) == 1:
                return True

        if config['win_by_corners']:
            # (0,0), (0, 4), (4, 0), (4,4))
            max = len(self._numbers[0])-1
            if self._numbers[0][0] == 0 and self._numbers[0][max] == 0 and self._numbers[max][0] == 0 and self._numbers[max][max] == 0:
                return True

        if config['win_by_all']:
            for i in range(5):
                for val in self._numbers[i]:
                    if val != 0:
                        return False
            return True

        return False

        # if set(self._numbers).length == 1:
        #     return True
        # else:
        #     return False
    def __str__(self):
        return f'{self._numbers}'
class Sheet(object):
    _boards = None
    def __init__(self, board_count):

        self._boards = Board.generate('modern')
    def mark_number(self, val):
        # we need to ask all boards for the number until one has it
        for board in self._boards:
            if board.mark_number(val):
                return True
        else:       
            return False
    
    def check_bingo(self):
        for board in self._boards:
            if board.check_bingo():
                return True
        else:
            return False
    
    def __str__(self):
        return f'{self._boards}'
class Player(object):
    _sheet = None
    _board = None
    _name = ''
    def __init__(self, name, boards=1):
        self._name = name
        if config['mode'] == 'classic':
            self._board = Board()
        else:
            # ask how many boards on the sheet
            self._sheet = Sheet(board_count=boards)
    def mark_number(self, val):
        return self._board.mark_number(val)
    
    def check_bingo(self):
        return self._board.check_bingo()
    def __str__(self):
        return f'{self._name} ({str(self._board)})'
class Game(object):
    players = []
    all_numbers = []
    remaining_numbers = []
    called_numbers = []
    is_won = False
    turn_count = 0
    
    
    def __init__(self):
        self.all_numbers = list(set(B + I + N + G + O))
        self.remaining_numbers = list(set(B + I + N + G + O))
        print(self.all_numbers)
        confirm = False
        player_count = 0
        # while not confirm:
        print('How many players?')
        player_count = int(input())
        # print('Is {player_count} players correct? y/n')
        # confirm_input = input()
        # if confirm_input == 'y':
        #     confirm = True

        for i in range(player_count):
            print(f'Enter player{i+1} name:')
            name_input = input()
            if name_input != '':
                confirm = True
                
                player = Player(name_input)
                self.players.append(player)
            
    def draw_number(self):
        import random
        return random.choice(self.remaining_numbers)
    def play(self):
        start = timer()

        while not self.is_won:
            num = self.draw_number()
            self.called_numbers.append(num)
            self.remaining_numbers.remove(num)
            print(f'Number drawn is: {num}')
            for player in self.players:
                marked = player.mark_number(num)
                if marked:
                    # print(f'{player._name} has the number {num}!')
                    self.is_won = player.check_bingo()
                                                                
                if self.is_won:
                    end = timer()
                    print(f'{end - start} seconds') # Time in seconds, e.g. 5.38091952400282
                    print(f'{player._name} called bingo! They won in {self.turn_count} moves. Against {len(self.players)-1} players!')
                    quit()
            self.turn_count +=1


# ...
# play()
def main():
    _game = Game()
    _game.play()

main()


    
