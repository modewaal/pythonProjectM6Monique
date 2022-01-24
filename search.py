"""
In the search class the AI-Player calculates its route to the finish using an A* algorithm.
The search class was based on tutorial 6 (https://github.com/M6AIP2021/tutorial-06-modewaal.git)
other algorithms than the A* algorithm were removed. highlight path was removed.
compute path was added: here the 10 steps are computed by the AI.
"""

import bisect
import random
from datetime import datetime


class Search:

    def __init__(self, maze):
        self.maze = maze
        random.seed(datetime.now())
        self.current_node = self.maze.start
        self.path_list = [self.current_node]

    def do_move(self):
        self.maze.reset_state()

        priority_queue = [self.maze.start]
        visited = []

        while len(priority_queue) > 0:
            self.current_node = priority_queue.pop(0)
            if self.current_node != self.maze.target:
                if self.current_node not in visited:
                    visited.append(self.current_node)
                    neighbours = self.current_node.get_neighbours()
                    fscore = self.current_node.get_distance() + 1  # (neighbour) distance from start
                    for next_node in neighbours:
                        if next_node not in visited:
                            gscore = next_node.manhattan_distance(self.maze.target)  # distance to target
                            score = gscore + fscore
                            if next_node not in priority_queue:
                                next_node.set_parent(self.current_node)
                                next_node.set_score(score)
                                bisect.insort_left(priority_queue, next_node)
                            elif fscore < next_node.get_distance():
                                next_node.set_parent(self.current_node)
                                next_node.set_score(score)
                                priority_queue.remove(next_node)
                                bisect.insort_left(priority_queue, next_node)
            else:
                break
        self.compute_path()
        if not self.path_list:
            return -1  # finish has been reached
        else:
            self.maze.set_source(self.path_list[0])  # set the current point to be the start of the next round
            return 1  # now it's the players turn

    def compute_path(self):
        # Compute the path, back to front.
        current_node = self.maze.target.parent
        self.path_list = []
        while current_node is not None and current_node != self.maze.start:
            self.path_list.append(current_node)
            current_node = current_node.parent

        self.path_list = self.path_list[-10:]  # get last 10 elements of the list, so the first 10 steps towards the target
        # print(self.path_list)  # check

