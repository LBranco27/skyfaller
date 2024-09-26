import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from shapes.cube import Cube
import random
import time
import config
import numpy as np
from loguru import logger

import freetype
import os
font_path = os.path.join(os.path.dirname(__file__), "assets/Roboto-Regular.ttf")

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
        self.start_time = time.time()
        self.font = freetype.Face(font_path)
        
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
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, config.width, config.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(90, config.width / config.height, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        self.configure_fog()

        mat_specular = [ 0.9, 0.9, 0.9, 1.0 ] #color of specular highlights
        mat_diffuse =[ 0.2, 0.8, 0.6, 1.0 ] #color of diffuse shading
        mat_ambient= [ 0.2, 0.9, 0.0, 1.0 ] #color of ambient light
        mat_shininess = [ 0.9 ] #the "shininess" of the specular highlight
 
        glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
        glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
        glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)

        light_position = [ 100.0, 100.0, 200.0, 1.0 ]
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)

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
        self.update_speed()
        for obs in config.obstacles:
            obs[1] += config.obstacle_speed
            if obs[1] > camera_y + 20:
                obs[1] = camera_y - config.obstacle_distance
                obs[0] = random.uniform(-20, 20)
                obs[2] = random.uniform(-20, 20)

    def update_speed(self):
        """
        Increases the speed of obstacles progressively over time.
        """
        elapsed_time = time.time() - self.start_time
        config.obstacle_speed = 0.005 + (elapsed_time * 0.0001)

    def _check_collision(self):
        """
        Checks if the player collides with any obstacles.

        Returns:
            bool: True if collision is detected, False otherwise.
        """
        for obs in config.obstacles:
            if np.all(np.abs(obs - config.player_pos) < config.player_size + config.obstacle_size):
                config.lives -= 1
                if config.lives <= 0:
                    config.game_over = True
                else:
                    self.shake_cube(obs)
                #print("OBS ", obs)
                #print("PLAYER ", config.player_pos)
                return True
        return False

    def shake_cube(self, obs):
        """
        Makes the cube tremble and change color when the player loses a life.
        """
        for _ in range(10):
            obs[0] += random.uniform(-0.5, 0.5)
            obs[2] += random.uniform(-0.5, 0.5)
            Cube(obs, config.obstacle_size, (1, 0, 0)).draw() 
            glfw.swap_buffers(self.window)
            time.sleep(0.05)
            
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

    def render_text(self, text, x, y, scale=30):
        self.font.set_char_size(scale * 64)
        glPushMatrix()

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()

        # Define uma projeção ortográfica com base no tamanho da janela para deixar os textos fixos
        glOrtho(0, config.width, 0, config.height, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glRasterPos2f(x * config.width, y * config.height)

        glPixelZoom(1, -1)

        glColor3f(1, 1, 1)

        pen_x = x * config.width
        for char in text:
            self.font.load_char(char)
            bitmap = self.font.glyph.bitmap
            width = bitmap.width
            rows = bitmap.rows
            glDrawPixels(width, rows, GL_LUMINANCE, GL_UNSIGNED_BYTE, bitmap.buffer)
            pen_x += self.font.glyph.advance.x >> 6
            glRasterPos2f(pen_x, y * config.height)

        glPixelZoom(1, 1) 
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

    def render_score(self, score):
        self.render_text(f'Pontuação: {score}   Vidas: {config.lives}', 0.05, 0.9)  

    
    def update_score(self):
        elapsed_time = time.time() - self.start_time
        config.score = int(elapsed_time * 10)  

    def render(self):
        """
        Renders the game screen.

        Returns:
            None
        """
        glClearColor(0.7, 0.9, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glRotate(90, 1, 0, 0)
        glTranslatef(0, -config.player_pos[1]-10, 0)

        config.player_pos[1] -= config.fall_speed

        print("PLAYER ", config.player_pos)
        camera_y = config.player_pos[1] - 3
        self._move_obstacles(camera_y)
        self._spawn_obstacles(camera_y)

        glLightfv(GL_LIGHT0, GL_POSITION, [config.player_pos[0], config.player_pos[1], config.player_pos[2]+5, 1.0])
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
        glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.01)

        player_cube = Cube(config.player_pos, config.player_size, (0, 1, 0))
        player_cube.draw()

        for obs in config.obstacles:
            obstacle_cube = Cube(obs, config.obstacle_size, (1,0,0))#random.uniform(config.obstacle_size, 3), (1, 0, 0))
            obstacle_cube.draw()

        if self._check_collision():
            logger.critical("Collision detected!\n\n")
            config.game_over = True

        self.update_score()
        self.render_score(config.score)
        
        glfw.swap_buffers(self.window)
        glfw.poll_events()
    
        #time.sleep(1 / 60) 