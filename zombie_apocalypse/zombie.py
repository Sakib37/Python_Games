# http://www.codeskulptor.org/#user39_QhwUYuZkB4_12.py
# http://www.codeskulptor.org/#user39_QhwUYuZkB4_13.py
#
# This prototype of the game can be used from the below link:
# http://www.codeskulptor.org/#user39_nv2HRXqLmpsz7Q4.py


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
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
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
        self._human_list *= 0
        self._zombie_list *= 0
        
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
        # replace with an actual generator
        for zombie in self._zombie_list:
            yield zombie 

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
        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        visited = poc_grid.Grid(self._grid_height, self._grid_width)
        max_distance = self._grid_height * self._grid_width
        distance_field = [[max_distance for dummy_col in range(self._grid_width)] 
                          for dummy_row in range(self._grid_height)]
        
        # boundary queue contains all the entity_type locations
        boundary = poc_queue.Queue()
        if entity_type == "zombie":
            for item in self.zombies():
                boundary.enqueue(item)
        elif entity_type == "human":
            for item in self.humans():
                boundary.enqueue(item)
        
        # Mark entity_type position as FULL and their distance from same entity_type as 0
        for entity_position in boundary:
            visited.set_full(entity_position[0], entity_position[1])
            distance_field[entity_position[0]][entity_position[1]] = 0 
            
        #while the boundary queue is not empty
        while boundary.__len__():
            current_cell = boundary.dequeue()
            neighbors = self.four_neighbors(current_cell[0], current_cell[1])
            
            for neighbor in neighbors:
                if visited.is_empty(neighbor[0], neighbor[1]) \
                and self.is_empty(neighbor[0], neighbor[1]):
                    visited.set_full(neighbor[0], neighbor[1])
                    boundary.enqueue(neighbor)
                    # distance of neighbor cell = distance of current cell + 1
                    distance_field[neighbor[0]][neighbor[1]] = \
                               distance_field[current_cell[0]][current_cell[1]] + 1
          
        return distance_field    
    
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        new_human_list = []
        obstacle = self._grid_height * self._grid_width
        for human in self.humans():
            # get all the eight possible move for that human
            neighbor_cells = self.eight_neighbors(human[0], human[1])
            
            # zombie distance in neighboring 8 cells
            distance_list = [zombie_distance[neighbor[0]][neighbor[1]] for neighbor in neighbor_cells 
                            if zombie_distance[neighbor[0]][neighbor[1]] != obstacle]
            max_distance = max(distance_list)
            
            # Effective possible locations to move
            if zombie_distance[human[0]][human[1]] >= max_distance:
                new_human_list.append(human)
                continue
            
            possible_move = [neighbor for neighbor in neighbor_cells
                            if zombie_distance[neighbor[0]][neighbor[1]] == max_distance]
            new_human_list.append(random.choice(possible_move))
        
        self._human_list = new_human_list
                                            
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        new_zombie_list = []
        obstacle = self._grid_height * self._grid_width
        for zombie in self.zombies():
            # get all four possible move for the zombie
            neighbor_cells = self.four_neighbors(zombie[0], zombie[1])
            
            # human distance in neighboring 4 cells 
            distance_list = [human_distance[neighbor[0]][neighbor[1]] for neighbor in neighbor_cells 
                            if human_distance[neighbor[0]][neighbor[1]] != obstacle]
            min_distance = min(distance_list)
            
            # Effective possible location to move
            if human_distance[zombie[0]][zombie[1]] <= min_distance:
                new_zombie_list.append(zombie)
                continue
            possible_move = [neighbor for neighbor in neighbor_cells
                            if human_distance[neighbor[0]][neighbor[1]] == min_distance]
            new_zombie_list.append(random.choice(possible_move))
        self._zombie_list = new_zombie_list

    

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

# poc_zombie_gui.run_gui(Zombie(30, 40))




