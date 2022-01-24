"""
Python Project M6 by Monique de Waal - s2564092
2022-01-23
AI&P - DR. M. GERHOLD

In a maze the AI-player (green block) has to get to the finish, the red block.
But, a player interferes with the AI, by changing the maze!
The player can change the maze each time after the AI has done 10 steps.
The player however, has not the full vision on the field,
The player has to look through a small window.
After the AI finishes the complex maze, VLC will start playing a cute doggo :)

The code of the maze was based on tutorial 6 of the AI&P course: https://github.com/M6AIP2021/tutorial-06-modewaal.git

The main class contains the game loop, updates the game and draws all the components.
some methods for event handling can also be found in the main class.
"""


import pygame
import sys
import time
from helpers.keyboard_handler import KeyboardHandler
from maze import Maze
from helpers.constants import Constants
from search import Search
from player import Player
from arduino import Arduino
import vlc


class Game:
    """
    Initialize PyGame and create a graphical surface to write. Similar
    to void setup() in Processing
    """

    def __init__(self):
        pygame.init()
        self.size = (Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT)
        self.screen = pygame.display.set_mode(self.size)
        self.keyboard_handler = KeyboardHandler()
        self.font = pygame.font.SysFont(pygame.font.get_fonts()[0], 64)
        self.time = pygame.time.get_ticks()
        self.maze = Maze(Constants.GRID_COLS, Constants.GRID_ROWS, self.size)
        self.maze.generate_maze()
        self.arduino = Arduino()
        self.player = Player(0, 0, self.maze, self.arduino)
        self.search = Search(self.maze)
        self.current_player = 0
        self.finish = vlc.MediaPlayer("media/dog.mp4")

    """
    Method 'game_loop' will be executed every frame to drive
    the display and handling of events in the background. 
    In Processing this is done behind the screen. Don't 
    change this, unless you know what you are doing.
    """

    def game_loop(self):
        current_time = pygame.time.get_ticks()
        delta_time = current_time - self.time
        self.time = current_time
        self.handle_events()
        self.draw_components()
        self.update_game(delta_time)

    """
    Method 'update_game' is there to update the state of variables 
    and objects from frame to frame.
    """

    def update_game(self, dt):
        if self.current_player == 0:  # AI turn
            self.current_player = self.search.do_move()
        elif self.current_player == 1:  # player turn
            self.current_player = self.player.do_move()
        elif self.current_player == -1:
            self.arduino.set_led(0, 0, 1)
            self.finish.play()
            time.sleep(14)
            self.finish.stop()
            self.arduino.handle_input()  # to check whether the LEDs changed to green
            exit()


    """
    Method 'draw_components' is similar is meant to contain 
    everything that draws one frame. It is similar to method
    void draw() in Processing. Put all draw calls here. Leave all
    updates in method 'update'
    """

    def draw_components(self):
        self.screen.fill([255, 255, 255])
        self.maze.draw_maze(self.screen)
        self.player.draw(self.screen, self.size)
        pygame.display.flip()

    def draw_score(self):
        text = self.font.render(str(self.maze.target.distance), True, (0, 0, 0))
        self.screen.blit(text, (self.size[0] / 2 - 64, 20))

    def reset(self):
        pass

    """
    Method 'handle_event' loop over all the event types and 
    handles them accordingly. 
    In Processing this is done behind the screen. Don't 
    change this, unless you know what you are doing.
    """

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.handle_key_down(event)
            if event.type == pygame.KEYUP:
                self.handle_key_up(event)
            if event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_pressed(event)
            if event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_released(event)

        x, y = self.arduino.handle_input()[0], self.arduino.handle_input()[1]
        x = x / 1024 * self.size[0]  # rescale to size of the screen
        y = y / 1024 * self.size[1]
        self.player.x, self.player.y = x, y

    """
    This method will store a currently pressed buttons 
    in list 'keyboard_handler.pressed'.
    """

    def handle_key_down(self, event):
        self.keyboard_handler.key_pressed(event.key)
        if event.key == pygame.K_m:
            print("Generating Maze")
            self.maze.generate_maze()
        if event.key == pygame.K_a:
            print("A*")
            self.search.do_move()

    """
    This method will remove a released button 
    from list 'keyboard_handler.pressed'.
    """

    def handle_key_up(self, event):
        self.keyboard_handler.key_released(event.key)

    """
    Similar to void mouseMoved() in Processing
    """

    def handle_mouse_motion(self, event):
        pass

    """
    Similar to void mousePressed() in Processing
    """

    def handle_mouse_pressed(self, event):
        if event.button == 1:
            self.player.left_mouse_button = True

    """
    Similar to void mouseReleased() in Processing
    """

    def handle_mouse_released(self, event):
        if event.button == 1:
            self.player.left_mouse_button = False


if __name__ == "__main__":
    game = Game()
    while True:
        game.game_loop()
