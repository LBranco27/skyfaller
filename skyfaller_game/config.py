import numpy as np

width, height = 800, 600
left_bound = -12.0
right_bound = 12.0
top_bound = 10.0
bottom_bound = -10.0

game_over = False

player_pos = np.array([0.0, 0.0, 0.0])
player_size = 1.0
fall_speed = 0.04

obstacles = []
obstacle_size = 2.0
obstacle_speed = 0.000005
max_obstacles = 30
obstacle_distance = 100

score = 0
lives = 3

