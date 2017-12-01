"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # Generates solved puzzle
        solved_puzzle = [[col + self.get_width() * row
                       for col in range(self.get_width())]
                      for row in range(self.get_height())]
        #print solved_puzzle
        # Zero tile is positioned at (i, j)
        if self.get_number(target_row, target_col) != 0:
            #print 'Failed 1'
            return False
        # All tiles in rows i+1 or below are positioned at their solved location
        if (target_row != self.get_height()-1):   
            for row in range(target_row+1, self.get_height()):
                for col in range(self.get_width()):
                    #print 'solved_value:', solved_puzzle[row][col]
                    #print 'self.get_number(target_row, col):', self.get_number(target_row, col)
                    if solved_puzzle[row][col] != self.get_number(row, col):
                        #print 'Failed 2'
                        return False
        # All tiles in row i to the right of position (i, j) are positioned
        # at their solved location
        if (target_col != self.get_width()-1):
            for col in range(target_col+1, self.get_width()):
                print 'solved_value:', solved_puzzle[target_row][col]
                print 'self.get_number(target_row, col):', self.get_number(target_row, col)
                if solved_puzzle[target_row][col] != self.get_number(target_row, col):
                    #print 'Failed 3'
                    return False
        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        # find the current location of target_tile
        current_row, current_col = self.current_position(target_row, target_col)
        move_string = ''
        # target tile is at target row
        if current_row == target_row:
            move_string = solve_interior_tile_same(self, target_row, target_col)
            return move_string
        # target tile is to the left of target_col
        if target_col > current_col:
            move_string = solve_interior_tile_left(self, target_row, target_col)
        # target tile is to the right in the target_col
        elif target_col < current_col:
            move_string = solve_interior_tile_right(self, target_row, target_col)
        # target tile and zero tile are in the same column
        current_row, current_col = self.current_position(target_row, target_col)
        zero_row = self.current_position(0, 0)[0]    
        # move zero tile to current location
        while zero_row > current_row:
            move = 'u'
            self.update_puzzle(move)
            move_string += move
            zero_row = self.current_position(0, 0)[0]        
        current_row, current_col = self.current_position(target_row, target_col)
        # Performs counter clockwise cycling to move into above target location
        while current_row < target_row:
            move = 'lddru'
            self.update_puzzle(move)
            move_string += move
            current_row, current_col = self.current_position(target_row, target_col)
        # Moves target tile into location and sets zero tile in next location
        move = 'ld'
        self.update_puzzle(move)
        move_string += move
        
        return move_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # Repositiion the target tile to the position (i-1, 1) and the zero tile to 
        # position (i-1, 0) using a process similar to that of solve_interior_tile
        move_string = ''
        current_row, current_col = self.current_position(target_row, 0)
        zero_row, zero_col = self.current_position(0, 0)
        # Target tile is directly above target row
        if (current_row - 1 == target_row) and (current_col == target_col):
            move = 'u'
            self.update_puzzle(move)
            move_string += move
        elif (current_row - 1 == target_row) and (current_row > 1):
            move 
    
        # Target tile is above target row
        elif current_row == target_row - 1 and current_col == 1 :
            move = 'uruldrdlurdluurddlur'
            self.update_puzzle(move)
            move_string += move
        # Target tile is to the right of target row:
        else:
            # Position zero tile to (i-1, 1)                    
            move_string += solve_col0_tile_bottom(self, target_row)            
            move = 'ruldrdlurdluurddlur'
            self.update_puzzle(move)
            move_string += move            
        zero_row, zero_col = self.current_position(0, 0)
        while zero_col < self.get_width()-1:
            move = 'r'
            self.update_puzzle(move)
            move_string += move
            zero_row, zero_col = self.current_position(0, 0)    
        return move_string

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        return False

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        return False

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        return ""

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        return ""
###########################################################
# Helper Functions
def make_random_puzzle(width, height):
    '''
    Makes a randomly generated fifteen puzzle of width and 
    height with the zero in the last place. 
    Returns the puzzle as a list of list.
    '''
    import random
    numbers = range(1, width*height)
    random.shuffle(numbers)
    numbers.insert(0, 0)
    puzzle = []
    while len(puzzle) < height:
        row = []
        while len(row) < width:
            row.append(numbers.pop())
        puzzle.append(row)  
    return puzzle

def solve_interior_tile_left(puzzle, target_row, target_col):
    '''
    Step 1 ONLY. Begins solving the puzzle when the target tile is to the 
    left of it's correct column. Returns a move string.
    '''
    zero_row, zero_col = puzzle.current_position(0, 0)
    current_row, current_col = puzzle.current_position(target_row, target_col)
    move_string = ''
    # move zero tile to right of target tile
    while zero_row > current_row:
        move = 'u'
        puzzle.update_puzzle(move)
        move_string += move
        zero_row -= 1
    # move zero_tile where target_tile is
    while zero_col > current_col:
        move = 'l'
        puzzle.update_puzzle(move)
        move_string += move
        zero_col -= 1
    current_row, current_col = puzzle.current_position(target_row, target_col)
    # move target_tile into target_col
    while current_col < target_col:
        move = 'drrul'
        puzzle.update_puzzle(move)
        move_string += move
        zero_col += 1
        current_row, current_col = puzzle.current_position(target_row, target_col)
    # move zero tile to below target col
    move = 'dr'
    puzzle.update_puzzle(move)
    move_string += move
    return move_string

def solve_interior_tile_right(puzzle, target_row, target_col):
    '''
    Step 1 ONLY. Begins solving the puzzle when the target tile is to the 
    right of it's correct column. Returns a move list.
    '''
    zero_row, zero_col = puzzle.current_position(0, 0)
    current_row, current_col = puzzle.current_position(target_row, target_col)
    move_string = ''
    # move zero tile to left of target tile
    while zero_row > current_row:
        move = 'u'
        puzzle.update_puzzle(move)
        move_string += move
        zero_row = puzzle.current_position(0, 0)[0]
    # move zero_tile where target_tile is
    while zero_col < current_col:
        move = 'r'
        puzzle.update_puzzle(move)
        move_string += move
        zero_col = puzzle.current_position(0, 0)[1]
    current_row, current_col = puzzle.current_position(target_row, target_col)
    ## Moves target tile into target col
    # Target tile is in top (0, j) row
    if current_row == 0:
        # move target tile to target col
        while current_col > target_col:
            move = 'dllur'
            puzzle.update_puzzle(move)
            move_string += move
            current_row, current_col = puzzle.current_position(target_row, target_col)
        # move zero tile to below target col
        move = 'dllddr'
        puzzle.update_puzzle(move)
        move_string += move
    # Target tile is in middle or bottom row (i>0, j)    
    else:      
        # move target tile to target col
        while current_col > target_col:
            move = 'ulldr'
            puzzle.update_puzzle(move)
            move_string += move
            current_row, current_col = puzzle.current_position(target_row, target_col)
        # move zero tile to below target col
        move = 'ullddr'
        puzzle.update_puzzle(move)
        move_string += move
    return move_string

def solve_interior_tile_same(puzzle, target_row, target_col):
    '''
    Step 1 ONLY. Begins solving the puzzle when the target tile is on the 
    it's correct column. Returns a move list.
    '''
    zero_col = puzzle.current_position(0, 0)[1]
    current_col = puzzle.current_position(target_row, target_col)[1]
    move_string = ''
    # move to right of target tile
    while zero_col > current_col + 1:
        move = 'l'
        puzzle.update_puzzle(move)
        move_string += move
        zero_col = puzzle.current_position(0, 0)[1]
    # move target tile to one column before target location
    while current_col < target_col-1:
        print puzzle
        move = 'lurrd'
        puzzle.update_puzzle(move)
        move_string += move
        zero_col = puzzle.current_position(0, 0)[1]
        current_col = puzzle.current_position(target_row, target_col)[1]
    move = 'l'
    puzzle.update_puzzle(move)
    move_string += move
    return move_string   

def solve_col0_tile_bottom(puzzle, target_row):
    '''
    Moves the target tile into (i-1, 1) when the target tile is NOT in the top row.
    Zero tile must be in (target_row, 0).
    Returns a move_string
    '''
    zero_row, zero_col = puzzle.current_position(0, 0)
    current_row, current_col = puzzle.current_position(target_row, 0)
    move_string = ''
    ## Moves target_tile to column 1
    if current_col > 1:
        # Target_tile is in top row
        if (current_row == 0):
            # Moves zero tile into current_row
            while zero_row > current_row:
                move = 'u'
                puzzle.update_puzzle(move)
                move_string += move
                zero_row = puzzle.current_position(0, 0)[0]
            # Moves zero_tile to position of target tile
            while zero_col < current_col:
                move = 'r'
                puzzle.update_puzzle(move)
                move_string += move
                zero_col = puzzle.current_position(0, 0)[1]
            # Cycles zero to move target tile into target col               
            while current_col > 1:
                move = 'dllur'
                puzzle.update_puzzle(move)
                move_string += move
                current_row, current_col = puzzle.current_position(target_row, 0)
            # Return zero_tile to (target_row, target_tile)
            # Move zero_tile below the target_tile
            move = 'd'
            puzzle.update_puzzle(move)
            move_string += move
            # Move zero_tile to target_col
            while zero_col > 0:
                move = 'l'
                puzzle.update_puzzle(move)
                move_string += move
                zero_col = puzzle.current_position(0, 0)[1]
            # Move zero_tile to target_row
            while zero_row < target_row - 1:
                move = 'd'
                puzzle.update_puzzle(move)
                move_string += move
                zero_row = puzzle.current_position(0, 0)[0]
        # Target_tile is in target_row-1
        elif current_row == target_row - 1:
            # Move zero_tile into current_row
            while zero_row > current_row:
                move = 'u'
                puzzle.update_puzzle(move)
                move_string += move
                zero_row = puzzle.current_position(0, 0)[0]
            # Move zero_tile into current_col
            while zero_col < current_col:
                move = 'r'
                move_string += move
                puzzle.update_puzzle(move)
                zero_col = puzzle.current_position(0, 0)[1]               
            # Moves zero_tile back to target location
            # Move zero_tile up
            move = 'u'
            move_string += move
            puzzle.update_puzzle(move)
            zero_row, zero_col = puzzle.current_position(0, 0)
            # Move zero_tile to target_col
            while zero_col > 0:
                move = 'l'
                puzzle.update_puzzle(move)
                move_string += move
                zero_col = puzzle.current_position(0, 0)[1]
            zero_row = puzzle.current_position(0, 0)[0]
            # Move zero_tile to target_row
            while zero_row < target_row-1:
                move = 'd'
                puzzle.update_puzzle(move)
                move_string += move
                zero_row = puzzle.current_position(0, 0)[0]
        # Target_tile is in middle row
        else:
            # Moves zero tile into current_row
            while zero_row > current_row:
                move = 'u'
                puzzle.update_puzzle(move)
                move_string += move
                zero_row = puzzle.current_position(0, 0)[0]
            # Moves zero_tile to position of target tile
            while zero_col < current_col:
                move = 'r'
                puzzle.update_puzzle(move)
                move_string += move
                zero_col = puzzle.current_position(0, 0)[1]
            # Cycles zero to move target tile into target col               
            while current_col > 1:
                move = 'dllur'
                puzzle.update_puzzle(move)
                move_string += move
                current_row, current_col = puzzle.current_position(target_row, 0)
            # Return zero_tile to (target_row, target_tile)
            # Move zero_tile below the target_tile
            move = 'd'
            puzzle.update_puzzle(move)
            move_string += move
            zero_row = puzzle.current_position(0, 0)[0]
            # Move zero_tile to target_col
            while zero_col > 0:
                move = 'l'
                puzzle.update_puzzle(move)
                move_string += move
                zero_col = puzzle.current_position(0, 0)[1]
            # Move zero_tile to target_row
            while zero_row < target_row:
                move = 'd'
                puzzle.update_puzzle(move)
                move_string += move
                zero_row = puzzle.current_position(0, 0)[0]
    ## Moves target_tile to target_row
    zero_row, zero_col = puzzle.current_position(0, 0)
    current_row, current_col = puzzle.current_position(target_row, 0)
    # Target_tile is in target_col but not target_row
    if current_row < target_row-1:
        # Move zero_tile to same row as target_tile
        while zero_row > current_row:
            move = 'u'
            puzzle.update_puzzle(move)
            move_string += move
            zero_row = puzzle.current_position(0, 0)[0]
        # Cycles zero_tile to move target_tile down column
        while current_row < target_row - 1:
            move = 'druld'
            puzzle.update_puzzle(move)
            move_string += move
            current_row, current_col = puzzle.current_position(target_row, 0)
    return move_string    
    
     

# Start interactive simulation
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))

random_game = make_random_puzzle(4, 4)
print random_game, '\n'
#random_game = [[2, 4, 15, 5], [10, 9, 3, 11], [7, 8, 14, 13], [6, 12, 1, 0]]
game = Puzzle(4, 4, random_game)
print game
game.solve_interior_tile(3,3)
print game
game.solve_interior_tile(3,2)
print game
game.solve_interior_tile(3,1)
print game
game.solve_col0_tile(3)
print game





