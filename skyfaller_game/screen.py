import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from shapes.cube import Cube
import random
import time
import config
import numpy as np
from loguru import logger

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

    def initialize(self):
        """
        Initializes the game screen.

        Returns:
            bool: True if initialization is successful, False otherwise.
        """
        if not glfw.init():
            return False
        self.window = glfw.create_window(config.width, config.height, "Endless Falling Game", None, None)
        if not self.window:
            glfw.terminate()
            return False
        glfw.make_context_current(self.window)
        glViewport(0, 0, config.width, config.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, config.width / config.height, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        return True

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
            if obs[1] > camera_y + 5:
                obs[1] = camera_y - 5
                obs[0] = random.uniform(-4, 4)

    def _check_collision(self):
        """
        Checks if the player collides with any obstacles.

        Returns:
            bool: True if collision is detected, False otherwise.
        """
        for obs in config.obstacles:
            if np.all(np.abs(obs[:2] - config.player_pos[:2]) < config.player_size + config.obstacle_size):
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
            x = random.uniform(-4, 4)
            y = camera_y - 5
            config.obstacles.append(np.array([x, y, -5]))
            self.last_spawn_time = current_time

    def render(self):
        """
        Renders the game screen.

        Returns:
            None
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        camera_y = config.player_pos[1] - 3
        glTranslatef(0, -camera_y, -10)

        config.player_pos[1] -= config.fall_speed

        self._move_obstacles(camera_y)
        self._spawn_obstacles(camera_y)

        player_cube = Cube(config.player_pos, config.player_size, (0, 1, 0))
        player_cube.draw()

        for obs in config.obstacles:
            obstacle_cube = Cube(obs, config.obstacle_size, (1, 0, 0))
            obstacle_cube.draw()

        if self._check_collision():
            logger.critical("Collision detected!")
            config.game_over = True

        glfw.swap_buffers(self.window)
        glfw.poll_events()
