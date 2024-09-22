import glfw
import config

class InputManager:
    """
    Class to manage input handling for the game.
    """

    def __init__(self, window):
        self.window = window

    def process_input(self):
        """
        Process the user input and update the player position accordingly.
        """
        if glfw.get_key(self.window, glfw.KEY_LEFT) == glfw.PRESS:
            config.player_pos[0] -= 0.1
        if glfw.get_key(self.window, glfw.KEY_RIGHT) == glfw.PRESS:
            config.player_pos[0] += 0.1
