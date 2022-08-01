import cv2
import numpy as np

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 720

class VideoWriter:
    def __init__(self, filename = 'video.avi', size = (2*WINDOW_WIDTH, 2*WINDOW_HEIGHT)):
        self.out = cv2.VideoWriter(filename,cv2.VideoWriter_fourcc(*'DIVX'), 60, size)
        self.height = size[1]
        self.width = size[0]

    def addGLframe(self, gl_frame):
        """
        assume the gl_frame is read with the following call:
        gl_frame = glReadPixels(0, 0, 2*WINDOW_WIDTH, 2*WINDOW_HEIGHT, GL_RGB, GL_FLOAT)
        """
        img = (gl_frame*255).astype('uint8')
        img = img.reshape(self.height, self.width, 3)
        img_flip = cv2.flip(img, 0)
        img_flip = cv2.cvtColor(img_flip, cv2.COLOR_RGB2BGR)
        self.out.write(img_flip)
    def close(self):
        self.out.release()
