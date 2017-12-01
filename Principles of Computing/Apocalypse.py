"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        
        poc_grid.Grid.clear(self)
        self._human_list = []
        self._zombie_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        
        self._zombie_list.append((row, col))
                        
    def num_zombies(self):
        """
        Return number of zombies
        """
        
        return len(self._zombie_list)
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zombie in self._zombie_list:
            yield zombie 
        return    

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        
        for human in self._human_list:
            yield human 
        return    
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        
        # 2.1 - Create a new grid visited of the same size as the original
        # grid and initalize its cells to be empty.
        visited = poc_grid.Grid(self._grid_height, self._grid_width)
        
        # 2.2 - Create a 2D list distance_field of the same size as the original
        # grid and initialize each of its entries to be the product of the height
        # times the width of the grid. (This value is larger than any possible 
        # distance.
        distance_field = [[ self._grid_height * self._grid_width \
                for dummy_col in range(self._grid_width)] \
                for dummy_row in range(self._grid_height)]
        
        # 2.3 - Create a queue boundary that is a copy of either the zombie list
        # of the human list. For cells in the queue, intiailize visited to be FULL
        # and distance_field to be zero. We reccomend that you use our Queue class.
        boundary = poc_queue.Queue()
        if entity_type == HUMAN:
            entity_list = self._human_list
        else:
            entity_list = self._zombie_list  
        for item in entity_list:
            boundary.enqueue(item)
            visited.set_full(item[0], item[1])
            distance_field[item[0]][item[1]] = 0
            
        
        # 2.3 - Implement a modified version of BFS described above. For each 
        # neighbor_cell in the inner loop, check whether the cell has not been 
        # visited and is passable. If so, update the visited grid and the boundary
        # queue as specified. In this case, also update the neighbor's distance
        # to be the distance to currrent_cell plus one.        
        while len(boundary) > 0:
            current_cell = boundary.dequeue()            
            neighbors = poc_grid.Grid.four_neighbors(self, current_cell[0], current_cell[1])           
            for neighbor_cell in neighbors:
                visit_cond = (visited.is_empty(neighbor_cell[0], neighbor_cell[1]))
                obstacle_cond = (self.is_empty(neighbor_cell[0], neighbor_cell[1]))                
                if (visit_cond and obstacle_cond):
                    visited.set_full(neighbor_cell[0], neighbor_cell[1])
                    boundary.enqueue(neighbor_cell)
                    distance_field[neighbor_cell[0]][neighbor_cell[1]] \
                        = distance_field[current_cell[0]][current_cell[1]] + 1
        
        return distance_field
       
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        
        best_locations = []
        for current_cell in self._human_list:
            best_location = current_cell
            best_dist = zombie_distance_field[current_cell[0]][current_cell[1]]
            neighbors = poc_grid.Grid.eight_neighbors(self, current_cell[0], current_cell[1])
            for neighbor_cell in neighbors:                
                neighbor_dist = zombie_distance_field[neighbor_cell[0]][neighbor_cell[1]]
                obstacle_cond =  self.is_empty(neighbor_cell[0], neighbor_cell[1])
                better_cond = neighbor_dist > best_dist
                if (obstacle_cond and better_cond):
                    best_dist = neighbor_dist
                    best_location = neighbor_cell
            best_locations.append(best_location)             
        self._human_list = best_locations
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        
        best_locations = []
        for current_cell in self._zombie_list:
            best_location = current_cell
            best_dist = human_distance_field[current_cell[0]][current_cell[1]]
            neighbors = poc_grid.Grid.four_neighbors(self, current_cell[0], current_cell[1])
            for neighbor_cell in neighbors:
                neighbor_dist = human_distance_field[neighbor_cell[0]][neighbor_cell[1]]
                if (neighbor_dist < best_dist):
                    best_dist = neighbor_dist
                    best_location = neighbor_cell
            best_locations.append(best_location)             
        self._zombie_list = best_locations

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Apocalypse(30, 40)) 