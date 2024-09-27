from OpenGL.GL import *
from PIL import Image

#unused
class TextureLoader:
    """
    Class to handle loading textures for Cube of Player and Obstacles, using the PIL library.
    """

    @staticmethod
    def load_texture(image_path):
        """
        Loads a texture from a file using PIL and binds it for OpenGL use.

        Args:
            image_path (str): The path to the image file.

        Returns:
            int: The texture ID for OpenGL.
        """
        try:
            # Load the image using PIL
            image = Image.open(image_path)
            image = image.transpose(Image.FLIP_TOP_BOTTOM)  # Flip the image for OpenGL compatibility
            img_data = image.convert("RGB").tobytes()  # Convert to byte data for OpenGL

            # Generate texture ID and bind it
            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)

            # Set texture parameters
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

            # Send the texture data to OpenGL
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

            return texture_id
        except IOError as e:
            print(f"Error loading texture: {e}")
            return None
