from OpenGL.GL import *
from PIL import Image
from ctypes import c_void_p
from gl_utils import Shader, Model
from gl_utils.GL_utils import perspective, InitGlfwWindow
import glfw
import numpy as np
import os
import glob
import cv2

VSHADER_PATH = "shaders/vertexShader.vs"
FSHADER_PATH = "shaders/fragmentShader.fs"

OBJ_FILE_PATH = "data/coke_normal.obj"#00300000_normal.obj"
CAMERA_FILE_PATH = "data/cameras_sphere.npz"
FACTOR = 1
WINDOW_WIDTH = 2313//FACTOR
WINDOW_HEIGHT = 3463//FACTOR


def load_K_Rt_from_P(P):
    out = cv2.decomposeProjectionMatrix(P)
    K = out[0]
    R = out[1]
    t = out[2]
    K = K / K[2, 2]
    intrinsics = np.eye(4)
    intrinsics[:3, :3] = K
    pose = np.eye(4, dtype=np.float32)
    pose[:3, :3] = R.transpose()
    pose[:3, 3] = (t[:3] / t[3])[:, 0]
    return intrinsics, pose

def projection_from_intrinsics(intrinsics, width, height):
    near = intrinsics[0,0]//FACTOR
    r = width - intrinsics[0,2]//FACTOR
    l = r - width
    t = height - intrinsics[1,2]//FACTOR
    b = t - height
    # scale near to 0.1
    factor = 10*near 
    near = near/factor
    r = r/factor
    l = l/factor
    t = t/factor
    b = b/factor
    far = near*10
    perspective = np.eye(4)
    perspective[0,0] = 2*near/(r-l)
    perspective[0,2] = (r+l)/(r-l)
    perspective[1,1] = 2*near/(t-b)
    perspective[1,2] = (t+b)/(t-b)
    perspective[2,2] = -(far+near)/(far-near)
    perspective[2,3] = -2*far*near/(far-near)
    perspective[3,2] = -1
    perspective[3, 3] = 0
    return perspective

def projection_from_image_size(width = 2313, height = 3423, near = 0.1, far = 10):
    projection = np.zeros((4,4))
    projection[0,0] = 2/width
    projection[0,2] = -1
    projection[1,1] = -2/height
    projection[1,2] = 1
    projection[2,2] = (far + near)/(far - near)
    projection[2,3] = -2*far*near/(far-near)
    projection[3,2] = 1
    return projection

def render(model, shader, projection, K, R, t, operation_code = 0):
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    shader.use()
    shader.setMat("projection", projection.T)
    shader.setMat("rotation", R.T)
    shader.setMat("K", K.T)
    shader.setVec("origin", t)
    shader.setInt("operationCode", operation_code)
    model.Draw()
    glUseProgram(0)
    gl_frame = glReadPixels(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, GL_RGB, GL_FLOAT)
    gl_frame = gl_frame.reshape(WINDOW_HEIGHT, WINDOW_WIDTH, 3)
    gl_frame = cv2.cvtColor(gl_frame, cv2.COLOR_BGR2RGB)
    return gl_frame

def get_cameras(camera_dict):
    world_mats = []
    scale_mats = []
    camera_num = 0
    world_mat = camera_dict.get('world_mat_{}'.format(camera_num))
    while world_mat is not None:
        world_mats.append(world_mat)
        scale_mats.append(camera_dict['scale_mat_{}'.format(camera_num)])
        camera_num += 1
        world_mat = camera_dict.get('world_mat_{}'.format(camera_num))
    return world_mats, scale_mats

def getKRt(P):
    P = P[:3, :4]
    intrinsics, pose = load_K_Rt_from_P(P)
    # get rotation
    R = np.linalg.inv(pose[:3,:3])
    t = pose[:3,-1]
    K = intrinsics[:3,:3]
    return K, R, t
if __name__ == '__main__':
    #main()
    os.makedirs('result', exist_ok=True)

    window = InitGlfwWindow(WINDOW_WIDTH, WINDOW_HEIGHT)
    model = Model(OBJ_FILE_PATH)
    print(model.position[:,0].min())
    print(model.position[:,0].max())
    print(model.position[:,1].min())
    print(model.position[:,1].max())
    print(model.position[:,2].min())
    print(model.position[:,2].max())
    shader = Shader(VSHADER_PATH, FSHADER_PATH)
    projection = projection_from_image_size()
    #while not glfw.window_should_close(window):
    camera_dict = np.load(CAMERA_FILE_PATH)
    world_mats, scale_mats = get_cameras(camera_dict)
    for i, camera_mats in enumerate(zip(world_mats, scale_mats)):
        world_mat, scale_mat = camera_mats
        P = world_mat#@scale_mat
        K, R, t = getKRt(P)
        # normal
        #gl_frame = render(model, shader, projection, K, R, t, operation_code=0)
        #gl_png = (gl_frame*255).astype(np.uint8)
        #cv2.imwrite(os.path.join('result', "{}_normal.pfm".format(i)), cv2.flip(gl_frame, 0))
        # world pos
        gl_frame = render(model, shader, projection, K, R, t, operation_code=1)
        #gl_png = (gl_frame*255).astype(np.uint8)
        cv2.imwrite(os.path.join('result', "{}_worldpos.pfm".format(i)), cv2.flip(gl_frame, 0))
    glfw.terminate()