from OpenGL.GL import *

class Cube:
    """
    A class representing a cube in 3D space.

    Attributes:
        position (tuple): The position of the cube in 3D space.
        size (float): The size of the cube.
        color (tuple): The color of the cube in RGB format.

    Methods:
        draw(): Draws the cube using OpenGL.
    """
    def __init__(self, position, size, color):
        self.position = position
        self.size = size
        self.color = color

    def draw(self):
            """
            Draw the cube using OpenGL.
            """
            glBegin(GL_QUADS)
            glColor3f(*self.color)

            vertices = [
                [self.position[0] - self.size, self.position[1] - self.size, self.position[2] + self.size],
                [self.position[0] + self.size, self.position[1] - self.size, self.position[2] + self.size],
                [self.position[0] + self.size, self.position[1] + self.size, self.position[2] + self.size],
                [self.position[0] - self.size, self.position[1] + self.size, self.position[2] + self.size],

                [self.position[0] - self.size, self.position[1] - self.size, self.position[2] - self.size],
                [self.position[0] + self.size, self.position[1] - self.size, self.position[2] - self.size],
                [self.position[0] + self.size, self.position[1] + self.size, self.position[2] - self.size],
                [self.position[0] - self.size, self.position[1] + self.size, self.position[2] - self.size],

                [self.position[0] - self.size, self.position[1] - self.size, self.position[2] - self.size],
                [self.position[0] - self.size, self.position[1] - self.size, self.position[2] + self.size],
                [self.position[0] - self.size, self.position[1] + self.size, self.position[2] + self.size],
                [self.position[0] - self.size, self.position[1] + self.size, self.position[2] - self.size],

                [self.position[0] + self.size, self.position[1] - self.size, self.position[2] - self.size],
                [self.position[0] + self.size, self.position[1] - self.size, self.position[2] + self.size],
                [self.position[0] + self.size, self.position[1] + self.size, self.position[2] + self.size],
                [self.position[0] + self.size, self.position[1] + self.size, self.position[2] - self.size],

                [self.position[0] - self.size, self.position[1] + self.size, self.position[2] - self.size],
                [self.position[0] + self.size, self.position[1] + self.size, self.position[2] - self.size],
                [self.position[0] + self.size, self.position[1] + self.size, self.position[2] + self.size],
                [self.position[0] - self.size, self.position[1] + self.size, self.position[2] + self.size],

                [self.position[0] - self.size, self.position[1] - self.size, self.position[2] - self.size],
                [self.position[0] + self.size, self.position[1] - self.size, self.position[2] - self.size],
                [self.position[0] + self.size, self.position[1] - self.size, self.position[2] + self.size],
                [self.position[0] - self.size, self.position[1] - self.size, self.position[2] + self.size],
            ]

            for i in range(6):
                glColor3f(*self.color)
                glVertex3f(*vertices[i * 4 + 0])
                glVertex3f(*vertices[i * 4 + 1])
                glVertex3f(*vertices[i * 4 + 2])
                glVertex3f(*vertices[i * 4 + 3])

            glEnd()
