"""
The class Maze generates a full maze based on depth first search.
This class is based on tutorial 6 (https://github.com/M6AIP2021/tutorial-06-modewaal.git)
redundant code was deleted (the mazes with fewer walls)
"""

import random
from datetime import datetime
from grid_element import GridElement


class Maze:
    """
        Generates a grid based maze based on GridElements
        This class also contains a search algorithm for
        A* star search to solve the generated mazes
        """

    def __init__(self, grid_size_x, grid_size_y, screen_size):
        self.grid_size = (grid_size_x, grid_size_y)
        self.cell_width = screen_size[0] / grid_size_x
        self.cell_height = screen_size[1] / grid_size_y
        self.grid = []
        for x in range(grid_size_x):
            self.grid.append([])
            for y in range(grid_size_y):
                self.grid[x].append(GridElement(x, y, (self.cell_width, self.cell_height)))
        self.start = self.grid[0][0]
        self.target = self.grid[-1][-1]
        self.reset_all()
        random.seed(datetime.now())

    """
    Resets the GridElements of the maze
    """

    def reset_all(self):
        for row in self.grid:
            for cell in row:
                cell.reset_neighbours()
        self.reset_state()
        return None

    def reset_state(self):
        for row in self.grid:
            for cell in row:
                cell.reset_state()
        self.start.set_distance(0)
        self.start.set_score(0)
        # print(self.start)
        self.start.set_color((0, 255, 0))
        # print(self.start.color)
        self.target.color = (240, 60, 20)
        return None

    def set_source(self, cell):
        if cell != self.target:
            self.start = cell
            self.reset_state()

    def set_target(self, cell):
        if cell != self.start:
            self.target = cell
            self.reset_state()

    def print_maze(self):
        transposed = list(zip(*self.grid))
        for row in transposed:
            print(row)
        return None

    def draw_maze(self, surface):
        for row in self.grid:
            for element in row:
                element.draw_grid_element(surface)
        return None

    def possible_neighbours(self, cell):
        neighbours = []
        if cell.position[0] > 0:  # North
            neighbours.append(self.grid[cell.position[0] - 1][cell.position[1]])
        if cell.position[0] < self.grid_size[0] - 1:  # East
            neighbours.append(self.grid[cell.position[0] + 1][cell.position[1]])
        if cell.position[1] < self.grid_size[1] - 1:  # South
            neighbours.append(self.grid[cell.position[0]][cell.position[1] + 1])
        if cell.position[1] > 0:  # West
            neighbours.append(self.grid[cell.position[0]][cell.position[1] - 1])
        return neighbours

    def del_link(self, cell1, cell2):
        if cell2 in cell1.neighbours:
            cell1.neighbours.remove(cell2)
        if cell1 in cell2.neighbours:
            cell2.neighbours.remove(cell1)
        return None

    def add_link(self, cell1, cell2):
        if cell1.manhattan_distance(cell2) == 1:
            cell1.neighbours.append(cell2)
            cell2.neighbours.append(cell1)
        return None

    """
     Generate the maze based on depth first search 
     """

    def generate_maze(self):
        self.reset_all()

        wait = [self.start]
        passed = set()
        while len(wait) > 0:
            current_element = wait.pop(-1)
            if current_element not in passed:
                passed.add(current_element)
                neighbours = self.possible_neighbours(current_element)  # Here we want to us all possible neighbours
                for cell in neighbours[:]:
                    if cell in passed:
                        neighbours.remove(cell)
                random.shuffle(neighbours)
                wait.extend(neighbours)
                for next_element in neighbours:
                    next_element.parent = current_element

                if current_element.parent is not None:  # The source has no parent
                    self.add_link(current_element.parent, current_element)

        # add a few random links
        for i in range(max(self.grid_size)):
            random_row = random.choice(self.grid)
            random_element = random.choice(random_row)
            possible = self.possible_neighbours(random_element)
            for cell in possible[:]:
                if cell in random_element.get_neighbours():
                    possible.remove(cell)
            if len(possible) > 0:
                random_neighbor = random.choice(possible)
                self.add_link(random_element, random_neighbor)

        self.reset_state()
        return None
