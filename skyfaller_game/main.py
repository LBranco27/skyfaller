import glfw
from screen import Screen
from input_manager import InputManager
import config

class Game:
    def __init__(self):
        self.screen = Screen()
        self.input_manager = None

    def run(self):
        if not self.screen.initialize():
            return

        self.input_manager = InputManager(self.screen.window)

        while not glfw.window_should_close(self.screen.window) and not config.game_over:
            self.input_manager.process_input()
            self.screen.render()

        glfw.terminate()

if __name__ == "__main__":
    game = Game()
    game.run()
