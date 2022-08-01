from OpenGL.GL import *
import glfw
import numpy as np
import time

WINDOW_HIEGHT = 600
WINDOW_WIDTH = 720

def perspective(fovy, aspect = WINDOW_WIDTH/WINDOW_HIEGHT, zNear = 0.1, zFar = 100):
    """
    Implementation of glm::perspective
    https://github.com/g-truc/glm/blob/0.9.5/glm/gtc/matrix_transform.inl#L218
    """
    assert(zFar != zNear), "zFar cannot be equal to zNear"
    tanHalfFovy = np.tan(fovy/2)
    Result = np.zeros((4, 4))

    Result[0,0] = 1/(aspect*tanHalfFovy)
    Result[1,1] = 1/tanHalfFovy
    Result[2,2] = - (zFar + zNear) / (zFar - zNear)
    Result[2,3] = -1
    Result[3,2] = -(2*zFar*zNear) / (zFar - zNear)
    return Result

class command_listener:
    def __init__(self, window, camera, deltaT_max = 0.1):
        self.deltaT_max = deltaT_max
        self.cam = camera
        self.window = window
        self.time = time.time()
    def __call__(self):
        current_time = time.time()
        deltaT = min(current_time - self.time, self.deltaT_max)
        self.time = current_time
        if glfw.get_key(self.window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(self.window, True)
        if (glfw.get_key(self.window, glfw.KEY_W) == glfw.PRESS):
            self.cam.MoveCamera('rotate_up', deltaT)
            #print(self.cam.GetPos())
            #print(deltaT)
            #print(self.cam.GetViewMatrix())
        if (glfw.get_key(self.window, glfw.KEY_S) == glfw.PRESS):
            self.cam.MoveCamera('rotate_down', deltaT)
            #print(self.cam.GetPos())
        if (glfw.get_key(self.window, glfw.KEY_A) == glfw.PRESS):
            self.cam.MoveCamera('rotate_left', deltaT)
            #print(self.cam.GetPos())
        if (glfw.get_key(self.window, glfw.KEY_D) == glfw.PRESS):
            self.cam.MoveCamera('rotate_right', deltaT)
            #print(self.cam.GetPos())
        if (glfw.get_key(self.window, glfw.KEY_UP) == glfw.PRESS):
            self.cam.MoveCamera('forward', deltaT)
        if (glfw.get_key(self.window, glfw.KEY_DOWN) == glfw.PRESS):
            self.cam.MoveCamera('backward', deltaT)

class interactive_lights:
    def __init__(self, window, deltaT_max = 0.1):
        self.deltaT_max = deltaT_max
        #self.light_dir = np.array([-0.5, -0.0, -1.0])
        self.light_radius = 0.2
        self.light_angle = np.pi
        self.light_angle2 = 0
        self.window = window
        self.time = time.time()
    def update(self):
        current_time = time.time()
        deltaT = min(current_time - self.time, self.deltaT_max)
        self.time = current_time
        #if glfw.get_key(self.window, glfw.KEY_ESCAPE) == glfw.PRESS:
        #    glfw.set_window_should_close(self.window, True)
        if (glfw.get_key(self.window, glfw.KEY_I) == glfw.PRESS):
            #self.light_radius += deltaT
            self.light_angle2 += deltaT
        if (glfw.get_key(self.window, glfw.KEY_K) == glfw.PRESS):
            #self.light_radius -= deltaT
            self.light_angle2 -= deltaT
        if (glfw.get_key(self.window, glfw.KEY_J) == glfw.PRESS):
            self.light_angle += deltaT
        if (glfw.get_key(self.window, glfw.KEY_L) == glfw.PRESS):
            self.light_angle -= deltaT
    def get_light_dir(self):
        return np.array([self.light_radius*np.cos(self.light_angle)*np.cos(self.light_angle2),
                         self.light_radius*np.sin(self.light_angle)*np.cos(self.light_angle2),
                         self.light_radius*np.sin(self.light_angle2)])
def InitGlfwWindow(width = WINDOW_WIDTH, height = WINDOW_HIEGHT):
    #InitGlfw()
    if not glfw.init():
        return
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3);
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3);
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE);
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE);
    window = glfw.create_window(width, height, "Opengl GLFW Window", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    return window
