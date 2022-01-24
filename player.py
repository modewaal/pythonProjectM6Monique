"""
The class Player lets the player generate a new maze by clicking.
When the player has done his move, it will be the AI its turn.
In the draw method the window for the player is made.
"""

import pygame


class Player:

    def __init__(self, x, y, maze, arduino):
        self.maze = maze
        self.arduino = arduino
        self.x = x
        self.y = y
        self.left_mouse_button = False
        self.color = (0, 0, 255)
        self.radius = 50
        self.previous_state = 0

    def do_move(self):
        if self.left_mouse_button:  # if the player hits the left mouse button, the maze will change.
            self.maze.generate_maze()
            state = 1
            if self.previous_state != state:
                self.previous_state = state
                self.arduino.set_led(0, 1, 0)  # turn yellow light on, new maze is generated
            return 0
        else:  # as long as the player is on turn, the AI will not move forward.
            state = 0
            if self.previous_state != state:
                self.previous_state = state
                self.arduino.set_led(1, 0, 0)  # turn red light on, nothing is happening
            return 1

    # draw the window for the player
    def draw(self, screen, size):
        layer = pygame.Surface((size[0], size[1]))  # create a new layer
        layer.fill((0, 0, 0))  # make it black
        layer.set_colorkey((0, 0, 255))  # anything blue on the layer will be transparent
        pygame.draw.rect(layer, self.color, (
            self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2))  # make a seek through
        screen.blit(layer, (0, 0))
