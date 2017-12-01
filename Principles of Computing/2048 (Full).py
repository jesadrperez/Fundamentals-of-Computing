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
    new_line = []
    for num in line:
        if num > 0:
            new_line.append(num)
    new_line = new_line+[0]*(len(line)-len(new_line))
    
    line = new_line[:]
    new_line = []
    
    num_one = None
    num_two = None
    for index in range(0,len(line)):
        if (num_one is None) and (index < len(line)-1):
            num_one = line[index]        
            continue
        if (num_one is None) and (index == len(line)-1):
            new_line.append(line[index])
            continue        
        if num_two is None:
            num_two = line[index]        
        if (num_one == num_two) and (num_one + num_two > 0):
            new_line.append(num_one+num_two)        
            num_one = None
            num_two = None        
        else:
            new_line.append(num_one)
            if index == len(line)-1:
                new_line.append(num_two)
                continue                
            num_one = num_two
            num_two = None
    new_line = new_line+[0]*(len(line)-len(new_line))
    return new_line

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        
        self._grid_height = grid_height
        self._grid_width = grid_width
        self.reset()
        self._dir = {}
        
        dummy_lst = []
        for tile in range(self.get_grid_width()):
            dummy_lst.append((0,tile))
        self._dir[UP] = dummy_lst
        
        dummy_lst = []
        for tile in range(self.get_grid_width()):
            dummy_lst.append((self.get_grid_height()-1,tile))
        self._dir[DOWN] = dummy_lst
        
        dummy_lst = []
        for tile in range(self.get_grid_height()):
            dummy_lst.append((tile,0))
        self._dir[LEFT] = dummy_lst
        
        dummy_lst = []
        for tile in range(self.get_grid_height()):
            dummy_lst.append((tile,self.get_grid_width()-1))
        self._dir[RIGHT] = dummy_lst
        

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        
        self._grid = [[0 for dummy_col in range(self._grid_width)]
                           for dummy_row in range(self._grid_height)]        
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """

        return str(self._grid)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        dummy_flag = False
        
        if direction < 3:
            num_steps = self.get_grid_height()
        else:
            num_steps = self.get_grid_width()
        
        #print "range(num_steps)", range(num_steps)
        #print "self._dir", self._dir[direction]
        for tile in self._dir[direction]:
            #dummy_idx = []
            dummy_line = []
            #print "tile", tile
            for step in range(num_steps):
                row = tile[0]+step*OFFSETS[direction][0]
                col = tile[1]+step*OFFSETS[direction][1]
                #dummy_idx.append((row, col))
                dummy_line.append(self.get_tile(row, col))
            #print "idx", dummy_idx
            #print "line", dummy_line
            dummy_new_line = merge(dummy_line)
            
            if dummy_line != dummy_new_line:
                    dummy_flag = True
            #print "new line", dummy_new_line
            for step in range(num_steps):
                row = tile[0]+step*OFFSETS[direction][0]
                col = tile[1]+step*OFFSETS[direction][1]
                self.set_tile(row, col, dummy_new_line[step])              
        
        if dummy_flag:
            self.new_tile()
                
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        dummy_count = 0
        while True:
            dummy_row = random.choice(range(self.get_grid_height()))
            dummy_col = random.choice(range(self.get_grid_width()))
            if self.get_tile(dummy_row, dummy_col) == 0:
                self.set_tile(dummy_row, dummy_col, random.choice([4] + [2]*9))                    
                break
            else:
                dummy_count = dummy_count + 1
            if dummy_count == 50:
                self.reset()
                break
                
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
    
#poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
#import user43_Of1rDhqbal_14 as poc_2048_testsuite
#poc_2048_testsuite.run_suite(TwentyFortyEight)

#game = TwentyFortyEight(3, 2)
#print "self._grid", game
#print game.move(UP)
#print "self._grid", game