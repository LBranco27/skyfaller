import numpy as np

width, height = 800, 600
game_over = False

player_pos = np.array([0.0, 5.0, -5.0])
player_size = 1.0
fall_speed = 0.1

obstacles = []
obstacle_size = 1.0
obstacle_speed = 0.000005
max_obstacles = 2
