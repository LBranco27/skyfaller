import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

from shapes.cube import Cube
import random
import time
import config
import numpy as np
from loguru import logger

import os
font_path = os.path.join(os.path.dirname(__file__), "assets/Roboto-Regular.ttf")

import pygame
from pygame import freetype

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
        self.spawn_interval = random.uniform(0.5, 1.5)
        self.start_time = time.time()
        
        pygame.init()
        freetype.init()
        self.font = freetype.SysFont(None, 24)  
    
    #initializations and configs
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
        
        self.setup_lighting()

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(90, config.width / config.height, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        
        self.configure_fog()

        return True

    def setup_lighting(self):
        """
        Configures the lighting in the scene with diffuse, ambient, and specular light.
        """
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        light_position = [0.0, 10.0, 10.0, 1.0]  
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)

        light_diffuse = [1.0, 1.0, 1.0, 1.0]  
        light_specular = [1.0, 1.0, 1.0, 1.0]  
        light_ambient = [0.2, 0.2, 0.2, 1.0]  

        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
        glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)

        mat_specular = [0.9, 0.9, 0.9, 1.0]  # color of specular highlights
        mat_shininess = [0.9]  # the "shininess" of the specular highlight
        glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
        glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)

        glEnable(GL_COLOR_MATERIAL)  # Enable color tracking
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)  # Set color to affect ambient and diffuse

    def load_texture(self, image_path):
        """
        Loads a texture from an image file and returns the texture ID.

        Args:
            image_path (str): The path to the image file.

        Returns:
            int: The OpenGL texture ID.
        """
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        surface = pygame.image.load(image_path)
        image_data = pygame.image.tostring(surface, "RGB", True)
        
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, surface.get_width(), surface.get_height(), 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        return texture

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

    # states of updates in game
    def update_speed(self):
        """
        Increases the speed of obstacles progressively over time.
        """
        elapsed_time = time.time() - self.start_time
        
        base_speed = 0.001 
        acceleration_factor = 0.00005 
        config.obstacle_speed = base_speed + (acceleration_factor * (elapsed_time ** 2))
        
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
            obs["position"][1] += config.obstacle_speed 
            if obs["position"][1] > camera_y + 20:  
                obs["position"][1] = camera_y - config.obstacle_distance
                obs["position"][0] = random.uniform(-20, 20) 
                obs["position"][2] = random.uniform(-20, 20) 

    
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
            x = random.uniform(-30, 30)  
            y = camera_y - random.uniform(10, 50)  
            z = random.uniform(-30, 30)  

            size = random.uniform(1.0, 6.0)  

            config.obstacles.append({
                "position": np.array([x, y, z]),
                "size": size
            })

            self.last_spawn_time = current_time
            self.spawn_interval = random.uniform(0.5, 1.5)

    #logic of game and collisions
    def limit_player_movement(self):
        if config.player_pos[0] < config.left_bound:
            config.player_pos[0] = config.left_bound
        elif config.player_pos[0] > config.right_bound:
            config.player_pos[0] = config.right_bound

        if config.player_pos[2] < config.bottom_bound:
            config.player_pos[2] = config.bottom_bound
        elif config.player_pos[2] > config.top_bound:
            config.player_pos[2] = config.top_bound
            
    def _check_collision(self):
        """
        Checks if the player collides with any obstacles and removes the collided obstacle.
        
        Returns:
            bool: True if collision is detected, False otherwise.
        """
        for i, obs in enumerate(config.obstacles):
            # Access the position from the obstacle dictionary
            obstacle_position = obs["position"]
            obstacle_size = obs["size"]

            # Check for collision between player and obstacle using positions and sizes
            if np.all(np.abs(obstacle_position - config.player_pos) < config.player_size + obstacle_size):
                config.lives -= 1
                config.obstacles.pop(i)
                logger.info(f"Obstacle {i} removed. Lives remaining: {config.lives}")
                
                self.shake_player()
                
                if config.lives <= 0:
                    config.game_over = True
                return True
        return False

    
    def shake_player(self):
        """
        Shakes the player cube to simulate a damage effect, changing its color to red during the shake.
        """
        original_pos = config.player_pos.copy()

        # Shake and change color to red during the shake
        glEnable(GL_COLOR_MATERIAL)  # Ensure color material is enabled
        for _ in range(10):
            config.player_pos[0] += random.uniform(-0.7, 0.7)  # Shake on the x-axis
            config.player_pos[2] += random.uniform(-0.7, 0.7)  # Shake on the z-axis

            # Set color to red during the shake
            glColor3f(1, 0, 0)  # Red color for the player
            player_cube = Cube(config.player_pos, config.player_size, (1, 0, 0))  # Pass the red color to Cube
            player_cube.draw()

            glfw.swap_buffers(self.window)
            glfw.poll_events()
            time.sleep(0.05)  # Small delay between shakes

        # Restore the original position and set color back to green
        config.player_pos = original_pos
        glColor3f(0, 1, 0)
        player_cube = Cube(config.player_pos, config.player_size, (0, 1, 0))  
        player_cube.draw()

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
    

            
    #renders
    def render_obstacles(self):
        """
        Renders the obstacles, adjusting their size dynamically.

        """
        for obs in config.obstacles:
            size = obs["size"]
            position = obs["position"]
            cube = Cube(position, size, (0, 0, 1))  
            cube.draw()
            
    def render_text(self, text, x, y):
        surface, _ = self.font.render(text, (255, 255, 255))
        text_data = pygame.image.tostring(surface, "RGBA", True)
        width, height = surface.get_size()

        glRasterPos2f(x, y)
        glDrawPixels(width, height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

    def render_text(self, text, x, y):
        surface, _ = self.font.render(text, (255, 255, 255))
        text_data = pygame.image.tostring(surface, "RGBA", True)
        width, height = surface.get_size()

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, config.width, 0, config.height, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glRasterPos2f(x, y)
        glDrawPixels(width, height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

    def render_score(self, score):
        self.render_text(f'Pontuação: {score}   Vidas: {config.lives}', 10, config.height - 30)
    
    def update_score(self):
        elapsed_time = time.time() - self.start_time
        config.score = int(elapsed_time * 5)  

    def render(self):
        """
        Renders the game screen.
        """
        # Clear the screen with a sky-blue color
        glClearColor(0.7, 0.9, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Reset transformations and set the view
        glLoadIdentity()
        glRotate(90, 1, 0, 0)
        glTranslatef(0, -config.player_pos[1] - 10, 0) 
        
        # Update the player's position (falling effect)
        config.player_pos[1] -= config.fall_speed

        # Ensure player stays within bounds
        self.limit_player_movement()

        # Handle obstacles: move them and spawn new ones if necessary
        camera_y = config.player_pos[1] - 3
        self._move_obstacles(camera_y)
        self._spawn_obstacles(camera_y)

        # Set the light position relative to the player
        glLightfv(GL_LIGHT0, GL_POSITION, [config.player_pos[0], config.player_pos[1], config.player_pos[2] + 5, 1.0])
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
        glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.01)

        # Draw the player cube (green)
        glEnable(GL_COLOR_MATERIAL)
        glColor3f(0, 1, 0)  # Green color for the player
        player_cube = Cube(config.player_pos, config.player_size, (0, 1, 0))
        player_cube.draw()

        # Draw all the obstacles with their specific sizes and positions
        self.render_obstacles()

        # Check for any collisions between the player and obstacles
        if self._check_collision():
            logger.critical("Collision detected!")

        # Update the score based on elapsed time and render it
        self.update_score()
        self.render_score(config.score)

        # Swap the front and back buffers to display the rendered frame
        glfw.swap_buffers(self.window)
        
        # Poll for input events (e.g., keypresses)
        glfw.poll_events()

        