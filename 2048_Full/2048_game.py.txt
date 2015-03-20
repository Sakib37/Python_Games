# http://www.codeskulptor.org/#user39_FohCc8NhL4lFu5o.py
# I used codeskulptor.org to build this code
# This is a simple form of the game 2048

"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4


# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    # replace with your code from the previous mini-project
    result_list = [0] * len(line)
    merge_idx = 0
    for element in line:
        if element:
            if not result_list[merge_idx]:
                result_list[merge_idx] = element
            elif result_list[merge_idx] == element:
                result_list[merge_idx] *= 2
                merge_idx += 1
            else:
                merge_idx += 1
                result_list[merge_idx] = element
    return result_list

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self._height = grid_height
        self._width = grid_width
        self.reset()
        self._initial_tile = {
                    UP   : [(0, dummy_col) 
                             for dummy_col in range(self._width)],
                    DOWN : [((self._height - 1), dummy_col) 
                             for dummy_col in range (self._width)],
                    LEFT : [(dummy_row, 0) 
                             for dummy_row in range(self._height)],
                    RIGHT: [(dummy_row, (self._width - 1)) 
                             for dummy_row in range(self._height)]}

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [([0] * self.get_grid_width()) 
                     for dummy_row in range(self.get_grid_height())]
        self.new_tile()
        self.new_tile()
        self.__str__()
        
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        board = ""
        for row in self._grid:
            board += str(row) + "\n"
        return board

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # set the length of column or row to iterate
        if direction == UP or direction == DOWN:
            num_step = self._height
        elif direction  == LEFT or direction == RIGHT:
            num_step = self._width
        
        is_changed = False
        for tile in self._initial_tile[direction]:
            tmp_list = []
            row = tile[0]
            col = tile[1]
            # putting direction corresponding column or row in tmp_list
            for item in range(num_step):
                tmp_list.append(self._grid[row][col])
                row += OFFSETS[direction][0]
                col += OFFSETS[direction][1]
            
            merged_list = merge(tmp_list)
            # putting the merged list in the grid
            row = tile[0]
            col = tile[1]

            for item in merged_list:
                previous_grid_item = self._grid[row][col]
                self._grid[row][col] = item
                if self._grid[row][col] != previous_grid_item:
                    is_changed = True
                row += OFFSETS[direction][0]
                col += OFFSETS[direction][1] 
                
        if is_changed:
            self.new_tile()
            
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # insert empty grid index in "empty_grid" list
        empty_grid = [] 
        for row_no, row in enumerate(self._grid):
            for col_no, element in enumerate(row):
                if element == 0:
                    empty_grid.append((row_no, col_no))
       
        
        rand_pos = random.choice(empty_grid)
        tmp_list = [2] * 9 + [4]
        
        self.set_tile(rand_pos[0], rand_pos[1], random.choice(tmp_list))
                
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]
                                                                                                        

poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
