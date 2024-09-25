import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from shapes.cube import Cube
import random
import time
import config
import numpy as np
from loguru import logger


def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)

    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        error_message = glGetShaderInfoLog(shader)
        raise RuntimeError(f"Shader compilation error: {error_message.decode()}")

    return shader


def create_shader_program(vertex_source, fragment_source):
    print('entrou')
    vertex_shader = compile_shader(vertex_source, GL_VERTEX_SHADER)
    fragment_shader = compile_shader(fragment_source, GL_FRAGMENT_SHADER)

    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)

    if not glGetProgramiv(program, GL_LINK_STATUS):
        print('pqp')
        error_message = glGetProgramInfoLog(program)
        raise RuntimeError(f"Shader program linking error: {error_message.decode()}")


    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    print('saiu')
    return program


class Screen:
    """
    Represents the game screen.

    Attributes:
        last_spawn_time (float): The time of the last obstacle spawn.
        spawn_interval (float): The interval between obstacle spawns.
        window: The GLFW window object.
    """

    def __init__(self):
        self.last_spawn_time = time.time()
        self.spawn_interval = 1.0
        self.lightPos_location = None
        self.viewPos_location = None
        self.lightColor_location = None
        self.objectColor_location = None

    def initialize(self):
        """
        Initializes the game screen.

        Returns:
            bool: True if initialization is successful, False otherwise.
        """
        if not glfw.init():
            return False
        self.window = glfw.create_window(config.width, config.height, "Skyfaller", None, None)
        if not self.window:
            glfw.terminate()
            return False
        glfw.make_context_current(self.window)
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, config.width, config.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(90, config.width / config.height, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        self.configure_fog()

        with open("shaders/vertex_shader.glsl", "r") as f:
            vertex_source = f.read()
        with open("shaders/fragment_shader.glsl", "r") as f:
            fragment_source = f.read()

        self.shader_program = create_shader_program(vertex_source, fragment_source)
        print(self.shader_program)
        glUseProgram(self.shader_program)

        self.lightPos_location = glGetUniformLocation(self.shader_program, "lightPos")
        self.viewPos_location = glGetUniformLocation(self.shader_program, "viewPos")
        self.lightColor_location = glGetUniformLocation(self.shader_program, "lightColor")
        self.objectColor_location = glGetUniformLocation(self.shader_program, "objectColor")

        # Defina valores para os uniformes
        glUniform3f(self.lightPos_location, 0.0, 10.0, 0.0)  # Posição da luz
        glUniform3f(self.viewPos_location, 0.0, 0.0, 5.0)   # Posição da câmera (ou do jogador)
        glUniform3f(self.lightColor_location, 1.0, 1.0, 1.0)  # Cor da luz
        glUniform3f(self.objectColor_location, 0.0, 1.0, 0.0)  # Cor do objeto (por exemplo, verde)

        return True

    def configure_fog(self):
        """

        Makes fog heheheehehe lmao.

        """
        # Enable fog
        glEnable(GL_FOG)

        # Set fog mode to linear (can also be GL_EXP or GL_EXP2)
        glFogi(GL_FOG_MODE, GL_LINEAR)

        # Set fog color (matching the background color or a slightly different tone)
        fog_color = [0.7, 0.9, 1.0, 1.0]
        glFogfv(GL_FOG_COLOR, fog_color)

        # Set the start and end distances for linear fog
        glFogf(GL_FOG_START, 20.0)  # Fog starts at a distance of 5 units
        glFogf(GL_FOG_END, 50.0)   # Fog ends at a distance of 20 units

        # Set fog density (if using GL_EXP or GL_EXP2)
        # glFogf(GL_FOG_DENSITY, 0.05)  # Optional for exponential fog modes

    def _move_obstacles(self, camera_y):
        """
        Moves the obstacles on the screen.

        Args:
            camera_y (float): The y-coordinate of the camera.

        Returns:
            None
        """
        for obs in config.obstacles:
            obs[1] += config.obstacle_speed
            if obs[1] > camera_y + 20:
                obs[1] = camera_y - config.obstacle_distance
                obs[0] = random.uniform(-20, 20)
                obs[2] = random.uniform(-20, 20)

    def _check_collision(self):
        """
        Checks if the player collides with any obstacles.

        Returns:
            bool: True if collision is detected, False otherwise.
        """
        for obs in config.obstacles:
            if np.all(np.abs(obs - config.player_pos) < config.player_size + config.obstacle_size):
                print("OBS ", obs)
                print("PLAYER ", config.player_pos)
                return True
        return False

    def _spawn_obstacles(self, camera_y):
        """
        Spawns new obstacles on the screen.

        Args:
            camera_y (float): The y-coordinate of the camera.

        Returns:
            None
        """
        current_time = time.time()
        if current_time - self.last_spawn_time > self.spawn_interval and len(config.obstacles) < config.max_obstacles:
            x = random.uniform(-20, 20)
            y = camera_y - config.obstacle_distance
            z = random.uniform(-20, 20)
            config.obstacles.append(np.array([x, y, z]))
            self.last_spawn_time = current_time

    def render(self):
        """
        Renders the game screen.

        Returns:
            None
        """
        glUseProgram(self.shader_program)
        glUniform3f(self.lightPos_location, 0.0, 10.0, 0.0)  # Atualiza a posição da luz
        glUniform3f(self.viewPos_location, config.player_pos[0], config.player_pos[1], 5.0)  # Posição da câmera

        glClearColor(0.7, 0.9, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glRotate(90, 1, 0, 0)
        glTranslatef(0, -config.player_pos[1]-10, 0)

        config.player_pos[1] -= config.fall_speed

        camera_y = config.player_pos[1] - 3
        self._move_obstacles(camera_y)
        self._spawn_obstacles(camera_y)

        player_cube = Cube(config.player_pos, config.player_size, (0, 1, 0))
        player_cube.draw()

        for obs in config.obstacles:
            obstacle_cube = Cube(obs, config.obstacle_size, (1,0,0))#random.uniform(config.obstacle_size, 3), (1, 0, 0))
            obstacle_cube.draw()

        if self._check_collision():
            logger.critical("Collision detected!")
            config.game_over = True

        glfw.swap_buffers(self.window)
        glfw.poll_events()
