"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

#import poc_fifteen_gui
import random

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
        # Zero tile is positioned at (i, j)
        if self.get_number(target_row, target_col) != 0:
            return False
        # All tiles in rows i+1 or below are positioned at their solved location
        if (target_row != self.get_height() - 1):   
            for row in range(target_row + 1, self.get_height()):
                for col in range(self.get_width()):
                    if solved_puzzle[row][col] != self.get_number(row, col):
                        return False
        # All tiles in row i to the right of position (i, j) are positioned
        # at their solved location
        if (target_col != self.get_width() - 1):
            for col in range(target_col + 1, self.get_width()):
                if solved_puzzle[target_row][col] != self.get_number(target_row, col):
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
        ## If the target_tile is not in the target_row
        if current_row != target_row:
             ## STEP 1 - Move the target_tile into the target_col. 
             # target_tile is to the left of target_col
             if current_col < target_col:
                  move_string += solve_interior_tile_left(self, target_row, target_col)
             # target_tile is to the right of target_col
             elif current_col > target_col:
                  move_string += solve_interior_tile_right(self, target_row, target_col)
             # target_tile is in target_col, so nothing is done
             ## STEP 2 - Move the target_tile into the target_row.
             current_row, current_col = self.current_position(target_row, target_col)
             move_string += move_and_update(self, move_vertically_to(target_row, current_row + 1))             
             move_string += move_and_update(self, bring_down(target_row - current_row, 'left'))
             ## STEP 3 - Move the zero_tile into the location of next target_tile.
             move_string += move_and_update(self, move_to_location(target_row - 1, 
               target_col, target_row, target_col - 1, 'hv'))
        else:
             move_string += move_and_update(self, move_horizontally_to(target_col, current_col + 1))
             move_string += move_and_update(self, bring_right(target_col - current_col, 'up'))
        return move_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        current_row, current_col = self.current_position(target_row, 0)
        zero_row, zero_col = self.current_position(0, 0)
        move_string = ''
        # Target_tile is in (target_row - 1, 0)
        if (current_row == target_row - 1) and (current_col == 0):
             move = 'u'
             zero_row, zero_col = move_zero(self, zero_row, zero_col, move)
             move_string += move
        ## Step 1 - Move target_tile into (target_row - 1, target_col + 1)
        else:             
             # Target_tile is to the left of target_col + 1
             if (current_col == 0):
                  move_string += solve_col0_tile_up(self, target_row)
             # Target_tile is to the right of target_col + 1
             elif (current_col > 1):
                  move_string += solve_col0_tile_right(self, target_row)
             # Target_tile is in target_col but current_row < target_row - 1
             ## Step 2 - Move target_tile into target_row - 1
             current_row, current_col = self.current_position(target_row, 0)
             if (current_row < target_row - 1):
                  move = move_to_location(target_row, 0, current_row + 1, current_col, 'vh')
                  move += bring_down(target_row - current_row - 1, 'right')
                  zero_row, zero_col = move_zero(self, target_row, 0, move)
                  move_string += move
                  move = move_to_location(zero_row, zero_col, target_row, 0, 'hv')
                  move_string += move_and_update(self, move)
             ## Step 3 - Cycle zero_tile to move target_tile into (target_row, target_col)
             move = 'u'
             move += 'ruldrdlurdluurddlur'
             move_string += move_and_update(self, move)
        ## Step 4 - Move zero_tile to (target_row - 1, self.get_width() - 1)
        zero_row, zero_col = self.current_position(0, 0)
        move = move_to_location(zero_row, zero_col, target_row - 1, self.get_width() - 1, 'hv')
        move_string += move_and_update(self, move)
        return move_string

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # Generates solved puzzle
        solved_puzzle = [[col + self.get_width() * row
                       for col in range(self.get_width())]
                      for row in range(self.get_height())]   
        # Check whether tile zero is at (0,j)
        zero_row, zero_col = self.current_position(0, 0)
        if (zero_row != 0) or (zero_col != target_col):        
            return False
        # Check that all tiles in row 0 to the right of position (0, j) are positioned
        # at their solved location
        if (target_col < self.get_width()):
            for col in range(target_col + 1, self.get_width()):
                if solved_puzzle[0][col] != self.get_number(0, col):
                    return False
        # Check that all tiles in row 1 to the right of position (1, j-1) are positioned
        # at their solved location
        if (target_col < self.get_width()):
            for col in range(target_col, self.get_width()):
                if solved_puzzle[1][col] != self.get_number(1, col):
                    return False
        # Check that all tiles in rows > 1 are positioned at their solved location
        if (target_col != 0):   
            for row in range(2, self.get_height()):
                for col in range(self.get_width()):
                    if solved_puzzle[row][col] != self.get_number(row, col):
                        return False   
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # Generates solved puzzle
        solved_puzzle = [[col + self.get_width() * row
                       for col in range(self.get_width())]
                      for row in range(self.get_height())]        
        # Check whether tile zero is at (1,j)
        zero_row, zero_col = self.current_position(0, 0)
        if (zero_row != 1) or (zero_col != target_col):        
            return False
        # Check that all tiles in row 1 to the right of position (1, j) are positioned
        # at their solved location
        if (target_col < self.get_width()):
            for col in range(target_col + 1, self.get_width()):
                if solved_puzzle[1][col] != self.get_number(1, col):
                    return False
        # Check that all tiles in rows > 1 are positioned at their solved location
        if (target_col != 1):   
            for row in range(2, self.get_height()):
                for col in range(self.get_width()):
                    if solved_puzzle[row][col] != self.get_number(row, col):
                        return False   
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        current_row, current_col = self.current_position(0, target_col)
        zero_row, zero_col = (0, target_col)
        move_string = ''
        # Target_tile is at (0, j-1)
        if (current_row == 0) and (current_col == target_col - 1):
             # Moves target_tile to (0, target_col)
             # Moves zero_tile to (1, target_col - 1)
             move = 'ld'
             move_string = move_and_update(self, move)
             return move_string
        # Target_tile is not in (0, j-1)
        # Move target_tile to (1, j-1)
        else:
             # Target_tile is (0, ?)
             if current_row == 0:
                  # Step 1 - Move zero_tile below target_tile
                  move = move_to_location(zero_row, zero_col, current_row + 1, current_col + 1, 'hv')
                  move += 'l'
                  # Step 2 - Move target_tile to target_row + 1
                  move += 'u'
                  move_string += move
                  zero_row, zero_col = move_zero(self, zero_row, zero_col, move)
                  current_row, current_col = self.current_position(0, target_col)
             # Target_tile is in (1, ?)
             # Step 1 - Move zero_tile to (current_row, current_col + 1)
             if current_col < target_col - 1:
                 move = move_to_location(zero_row, zero_col, current_row, current_col + 1, 'hv')
                 # Step 2 - Move target_tile to (1, j-1)
                 move += bring_right(target_col - current_col - 1, 'up')
                 move_string += move_and_update(self, move)
             # Target_tile is in (1, target_col - 1)
             else: 
                 move = move_to_location(zero_row, zero_col, current_row, current_col - 1, 'hv')
                 move_string += move_and_update(self, move)
             # Zero_ tile is now at (1, target_col - 2)
             # Step 3 - Use cyclic movements to bring target_tile to (0, target_col)
             move = 'urdlurrdluldrruld'
             move_string += move_and_update(self, move)
        return move_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        current_row, current_col = self.current_position(1, target_col)
        zero_col = target_col
        move_string = ''
        # Target_tile is one tile to the left of (1, target_col)
        if (current_row == 1) and (current_col == target_col - 1):
            move = 'lur'
            move_string = move_and_update(self, move)
            return move_string
        # Target_tile is one tile above (1, target_col)
        if (current_row == 0) and (current_col == target_col):
            move = 'u'
            move_string = move_and_update(self, move)
            return move_string        
        # Target_tile is in row 0
        if current_row == 0:
             # Step 1 - Move zero_tile to the same row as target_tile
             move = 'u'
             # Step 2 - Move zero_tile to the right of target_tile
             move += move_horizontally_to(zero_col, current_col + 1)
             # Step 3 - Move target_tile into (0, target_col)
             move += bring_right(target_col - current_col, 'down')
             # Step 4 - Move zero_tile to below target_tile
             move += 'dr'
             # Step 5 - Move target_tile to (1, target_col) and zero_tile to
             # (0, target_col)
             move += 'u'
             move_string = move_and_update(self, move)
        # Target_tile is in row 1
        else:
             # Step 1 - Move zero_tile to the right of target_tile
             move = move_horizontally_to(zero_col, current_col + 1)
             # Step 2 - Move target_tile into target_col
             move += bring_right(target_col - current_col, 'up')
             # Step 3 - Move zero_tile into (0, target_col)
             move += 'ur'
             move_string = move_and_update(self, move)
        return move_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # Move zero_tile to (0,0)
        move_string = move_and_update(self, 'lu')
        # Checks whether puzzle if solved if it isn't then does rotation till it is
        while (not self.row0_invariant(0)):
            move_string += move_and_update(self, 'rdlu')
        return move_string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        move_string = ''
        if not self.row0_invariant(0):
             move_string += check_zero(self)
             move_string += solve_step1(self)
             move_string += solve_step2(self)
             move_string += self.solve_2x2()
        return move_string

###########################################################
# Solver Helper Functions
def solve_interior_tile_left(puzzle, target_row, target_col):
     '''
     Moves the target_tile to the target_col.
     Returns the move as a str
     '''
     current_row, current_col = puzzle.current_position(target_row, target_col)
     zero_row, zero_col = puzzle.current_position(0, 0)
     move_string = ''
     # Move the zero_tile to the same row and right of the target_tile, that is
     # (current_row, current_col - 1).
     move_string += move_to_location(zero_row, zero_col, current_row, current_col + 1, 'vh')
     move_string += bring_right(target_col - current_col, 'down')
     zero_row, zero_col = move_zero(puzzle, zero_row, zero_col, move_string) 
     # Return the zero_tile to (target_row, target_col)
     move = move_to_location(zero_row, zero_col, target_row, target_col, 'vh')
     move_string += move_and_update(puzzle, move)
     return move_string

def solve_interior_tile_right(puzzle, target_row, target_col):
     '''
     Moves the target_tile to the target_col.
     Returns the move as a str
     '''
     current_row, current_col = puzzle.current_position(target_row, target_col)
     zero_row, zero_col = puzzle.current_position(0, 0)
     move_string = ''
     # Move the zero_tile to the same row and left of the target_tile, that is
     # (current_row, current_col - 1).
     move_string += move_to_location(zero_row, zero_col, current_row, current_col - 1, 'vh')
     if current_row == target_row - 1:
          move_string += bring_left(current_col - target_col, 'up')
     else:
          move_string += bring_left(current_col - target_col, 'down')
     zero_row, zero_col = move_zero(puzzle, zero_row, zero_col, move_string) 
     # Return the zero_tile to (target_row, target_col)
     if zero_row == 0:
          move = move_to_location(zero_row, zero_col, zero_row + 1, 0, 'vh')
          move_string += move
          zero_row, zero_col = move_zero(puzzle, zero_row, zero_col, move)
          move = move_to_location(zero_row, zero_col, target_row, target_col, 'vh')
          move_string += move_and_update(puzzle, move)
     else:
          move = move_to_location(zero_row, zero_col, zero_row - 1, 0, 'vh')
          move_string += move
          zero_row, zero_col = move_zero(puzzle, zero_row, zero_col, move)
          move = move_to_location(zero_row, zero_col, target_row, target_col, 'vh')
          move_string += move_and_update(puzzle, move)          
     return move_string        

def solve_col0_tile_right(puzzle, target_row):
     '''
     Moves the target_tile into col 1.
     Returns the move as a str.
     '''
     current_row, current_col = puzzle.current_position(target_row, 0)
     zero_row, zero_col = puzzle.current_position(0, 0)
     move_string = ''
     # Move the zero_tile to the same row and left of the target_tile, that is
     # (current_row, current_col - 1).
     move_string += move_to_location(zero_row, zero_col, current_row, current_col - 1, 'vh')
     if current_row == target_row - 1:
          move_string += bring_left(current_col - 1, 'up')
     else:
          move_string += bring_left(current_col - 1, 'down')
     zero_row, zero_col = move_zero(puzzle, zero_row, zero_col, move_string) 
     # Return the zero_tile to (target_row, target_col)     
     if zero_row == 0:
          move = move_to_location(zero_row, zero_col, zero_row + 1, 0, 'vh')
          move_string += move
          zero_row, zero_col = move_zero(puzzle, zero_row, zero_col, move)
          move = move_to_location(zero_row, zero_col, target_row, 0, 'vh')
          move_string += move_and_update(puzzle, move)
     else:
          move = move_to_location(zero_row, zero_col, zero_row - 1, 0, 'vh')
          move_string += move
          zero_row, zero_col = move_zero(puzzle, zero_row, zero_col, move)
          move = move_to_location(zero_row, zero_col, target_row, 0, 'vh')
          move_string += move_and_update(puzzle, move)          
     return move_string           

def solve_col0_tile_up(puzzle, target_row):
     '''
     Moves the target_tile into col 1.
     Returns the move as a str.
     '''
     current_row = puzzle.current_position(target_row, 0)[1]
     move_string = ''
     # Move zero_tile to (target_row + 1, 1)
     move = 'ur'
     # Move zero_tile to the right of target_tile
     move += move_vertically_to(target_row - 1, current_row)
     # Move zero_tile to current_row, moving target_tile left into target_col + 1
     move += 'l'
     # Move zero_tile to the back to (target_row, target_col)
     move += move_vertically_to(current_row, target_row)
     # Perform moves
     move_string += move_and_update(puzzle, move)
     return move_string
       
###########################################################     
# Helper Functions
def make_random_puzzle(width, height):
    '''
    Makes a randomly generated fifteen puzzle of width and 
    height with the zero in the last place. 
    Returns the puzzle as a list of list.
    '''
    numbers = range(1, width*height)
    numbers = list(numbers)
    random.shuffle(numbers)
    numbers.insert(0, 0)
    puzzle = []
    while len(puzzle) < height:
        row = []
        while len(row) < width:
            row.append(numbers.pop())
        puzzle.append(row)  
    return puzzle

def make_solved_puzzle(width, height):
     '''
     Makes a solved fifteen puzzle object of width and height.
     Returns a fifteen puzzle object.
     '''
     # Generates solved puzzle
     solved_puzzle = [[col + width * row
                       for col in range(width)]
                      for row in range(height)]
     return Puzzle(height, width, solved_puzzle)

def randomize_puzzle(solved_puzzle, num_moves):
     '''
     Shuffles the tiles of solved_puzzle by applying a random move num_moves times.
     Returns the shuffles fifteen puzzle object.
     '''
     zero_row, zero_col = (0, 0)
     count = 1     
     while count < num_moves:
        # Get move to try and update zero_tile's location
        move = random.choice('urdl')
        if check_move(solved_puzzle, zero_row, zero_col, move):
            zero_row, zero_col =  move_zero(solved_puzzle, zero_row, zero_col, move)
            count += 1
     solved_puzzle.update_puzzle(move_to_location(zero_row, zero_col, solved_puzzle.get_height()-1, solved_puzzle.get_width()-1, 'hv'))       
     return solved_puzzle        

def check_move(puzzle, zero_row, zero_col, move):
    ''' 
    Checks to see if move is legal.
    Returns True if legal.
    '''
    zero_row, zero_col = update_locations(zero_row, zero_col, move)
    if move == 'l' or move == 'r':
          if -1 < zero_col < puzzle.get_width():
               return True
    else:
          if -1 < zero_row < puzzle.get_height():
               return True
    return False

def move_and_update(puzzle, move):
     '''
     Performs the move (a string of directions) on puzzle
     Returns move as str.
     '''
     puzzle.update_puzzle(move)
     return move

def move_up(current_row):
     '''
     Calculates the number of moves need to move all the way up to i=0 from
     current_row.
     Returns a move.
     '''
     if current_row == 0:
          return ''
     else:
        return 'u' + move_up(current_row - 1)

def move_left(current_col):
     '''
     Calculates the number of moves need to move all the way up to j=0 from
     current_col.
     Returns a move.
     '''
     if current_col == 0:
          return ''
     else:
        return 'l' + move_left(current_col - 1)
   
def move_down(height, current_row):     
     '''
     Calculates the number of moves need to move all the way down to i=height from
     current_row.
     Returns a move.
     '''
     if current_row == height - 1:
          return ''
     else:
        return 'd' + move_down(height, current_row + 1)
   
def move_right(width, current_col):
     '''
     Calculates the number of moves need to move all the way down to j=width from
     current_row.
     Returns a move.
     '''
     if current_col == width - 1:
          return ''
     else:
        return 'r' + move_right(width, current_col + 1)

def update_locations(zero_row, zero_col, move):
     '''
     Calculates the new location of the zero_tile after move is perfromed.
     Returns zero_row and zero col
     '''
     for direction in move:
          if direction == 'u':
               zero_row -= 1
          elif direction == 'd':
               zero_row += 1
          elif direction == 'l':
               zero_col -= 1
          else:
               zero_col += 1
     return zero_row, zero_col               

def move_vertically_to(current_row, target_row):
     '''
     Moves the zero tile from current_row to target_row.
     Returns this move as str.
     '''
     if (current_row - target_row) > 0:
          return 'u'+ move_vertically_to(current_row - 1, target_row)
     elif (current_row - target_row) < 0:
          return 'd' + move_vertically_to(current_row + 1, target_row)
     else:
          return ''

def move_horizontally_to(current_col, target_col):
     '''
     Moves the zero tile from current_col to target_col.
     Returns this move as str.
     '''
     if (current_col - target_col) > 0:
          return 'l'+ move_horizontally_to(current_col - 1, target_col)
     elif (current_col - target_col) < 0:
          return 'r' + move_horizontally_to(current_col + 1, target_col)
     else:
          return '' 

def move_to_location(current_row, current_col, target_row, target_col, pattern):
     '''
     Generates the move to move from (current_row, current_col) to 
     (target_row, target_col) using pattern. Pattern is which direction to move first.
     Returns this move as a str.
     '''
     if pattern == 'vh':
          return move_vertically_to(current_row, target_row) + move_horizontally_to(current_col, target_col)
     else:
          return move_horizontally_to(current_col, target_col) + move_vertically_to(current_row, target_row)

def bring_down(times, side):
     '''
     Generates the move used to move down the target_tile by the zero_tile by moving into
     the target_tile location and looping back under it. Side tells it which side (left or 
     right) to come back down. Zero_tile must be below target_tile at start and ends 
     above it when done. 
     Returns a str.
     '''
     if times == 0:
          return ''          
     elif times == 1:
          return 'u'
     else:
          if side == 'left':
               return 'ulddr' + bring_down(times - 1, 'left')
          elif side == 'right':
               return 'urddl' + bring_down(times - 1, 'right')
          
def bring_right(times, side):
     '''
     Generates the move used to move right the target_tile by the zero_tile by moving into
     the target_tile location and loop back left of it. Side tells it which sides
     (above or below) to come back. Zero_tile must be to the left at start and ends
     to the right when done.
     Returns a str.
     '''
     if times == 0:
          return ''          
     elif times == 1:
          return 'l'
     else:
          if side == 'up':
               return 'lurrd' + bring_right(times - 1, 'up')
          elif side == 'down':
               return 'ldrru' + bring_right(times - 1, 'down')

def bring_left(times, side):
     '''
     Generates the move used to move left the target_tile by the zero_tile by moving into
     the target_tile location and loop back right of it. Side tells it which sides
     (up or down) to come back. Zero_tile must be to the right at start and ends
     to the left when done.
     Returns a str.
     '''
     if times == 0:
          return ''          
     elif times == 1:
          return 'r'
     else:
          if side == 'up':
               return 'rulld' + bring_left(times - 1, 'up')
          elif side == 'down':
               return 'rdllu' + bring_left(times - 1, 'down')

def move_zero(puzzle, zero_row, zero_col, move):
     '''
     Makes move on puzzle and updates the location of zero_tile based on move.
     Returns zero_row, zero_col
     '''
     puzzle.update_puzzle(move)
     return update_locations(zero_row, zero_col, move)

def solve_step1(puzzle):
    '''
    Solves the bottom m-2 rows of the puzzle.
    Returns the moves as a str
    '''
    move_string = ''
    # Step 1 - Solve the bottom m−2 rows of the puzzle in a row by row manner from bottom to top.
    rows = range(2, puzzle.get_height())
    rows.reverse()
    for row in rows:
        # Each individual row will be solved in a right to left order.
        cols = range(0, puzzle.get_width())
        cols.reverse()
        for col in cols:
            assert puzzle.lower_row_invariant(row, col)
            if col > 0:
                move_string += puzzle.solve_interior_tile(row, col)
            else:
                move_string += puzzle.solve_col0_tile(row)
    return move_string            
    
def solve_step2(puzzle):
    '''
    Step 2 - Solve the rightmost n−2 columns of the top two rows of the puzzle 
    (in a right to left order).
    '''
    move_string = ''    
    # Step 2 - Solve the rightmost n−2 columns of the top two rows of the puzzle (in a right to left order).
    cols = range(2, puzzle.get_width())
    cols.reverse()
    for col in cols:
        # Each column consists of two unsolved positions and will be solved in a bottom to top order.
        rows = range(0, 2)
        rows.reverse()        
        for row in rows:
            print row, col
            if row == 0:                
                move_string += puzzle.solve_row0_tile(col)
            elif row == 1:
                move_string += puzzle.solve_row1_tile(col)
            print puzzle   
    return move_string

def check_zero(puzzle):
     '''
     Checks whether the zero_tile is at (n, m) to began solving the puzzle. If it
     isn't then it moves the zero_tile into position. 
     Returns the moves as a str.
     '''
     if puzzle.lower_row_invariant(puzzle.get_height()-1, puzzle.get_width()-1):
          return ''
     else:
          zero_row, zero_col = puzzle.current_position(0, 0)
          move = move_to_location(zero_row, zero_col, puzzle.get_height()-1, puzzle.get_width()-1, 'vh')
          return move_and_update(puzzle, move)