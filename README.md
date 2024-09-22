# 🎮 Skyfaller

## 🛠️ Introduction
This is an endless falling game built using OpenGL and GLFW. The player navigates a falling character while avoiding obstacles that spawn from above. The game provides a simple but engaging experience with real-time 3D graphics.

## 📦 Installation

To set up the project and download all required libraries, use the following command:

```
make install
```

This command will create a virtual environment and install all necessary dependencies listed in 📜`requirements.txt`. 

### 📜 Note
Whenever you use a new library (e.g., `pip install <library>`), ensure to add it to `requirements.txt` to keep the project organized and maintainable.

## 🚀 System Overview

### 🖥️ Code Explanation
The core functionality of the game includes the following key components:

- **Player Attributes**: The player character has attributes such as position, size, and fall speed.
- **Obstacle Management**: Obstacles are generated randomly and move towards the player, creating a challenge.
- **Collision Detection**: The game checks for collisions between the player and obstacles to determine if the game is over.
- **Game Loop**: The main loop handles player movement, obstacle spawning, and rendering.

## 🏁 Conclusion
27. Happy coding! 🎉
