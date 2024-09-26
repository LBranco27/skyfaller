import glfw

from input_manager import InputManager
import config
import moderngl_window as mglw

from screen import Screen


class Game(mglw.WindowConfig):
    window_size = 700, 400
    resource_dir = 'shaders'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.quad = mglw.geometry.quad_fs()
        self.prog = self.load_program(vertex_shader = 'vertex_shader.glsl',
                                      fragment_shader = 'fragment_shader.glsl')
        self.set_uniform('resolution', self.window_size)
        self.texture = self.load_texture_2d('game_over.jpeg')
        self.texture.use(0)

    def set_uniform(self, u_name, u_value):
        try:
            self.prog[u_name] = u_value
        except KeyError:
            print(f'uniform: {u_name} - not used in shader')

    def render(self, time, frame_time):
        if not config.game_over:
            exit()
        self.ctx.clear()
        self.set_uniform('time', time)
        self.set_uniform('gameOverTexture', 0)
        self.quad.render(self.prog)

def run(screen):
    if not screen.initialize():
        return

    input_manager = InputManager(screen.window)

    while not glfw.window_should_close(screen.window) and not config.game_over:
        input_manager.process_input()
        screen.render()

    glfw.terminate()

if __name__ == "__main__":
    run(Screen())
    mglw.run_window_config(Game)
