import numpy as np

YAW = np.pi #-np.pi/2
PITCH = 0.0
SPEED = 10.0
ROTATE_SPEED = 0.25
ZOOM = np.pi/4

WORLD_UP = np.array([0.0, 1.0, 0.0])
#FRONT_VEC = np.array([0.0, 0.0, -1.0])

default_specs = {
    'world_up'  :WORLD_UP,
    #'front_vec' :FRONT_VEC,
    'yaw'         :YAW,
    'pitch'       :PITCH,
    'speed'       :SPEED,
    'rotate_speed':ROTATE_SPEED,
    'zoom'        :ZOOM
}

class Camera:
    def __init__(self, position = np.zeros(3), specs = default_specs):
        self.position           = position
        #self.up_vec             = specs['up_vec']
        #self.front_vec          = specs['front_vec']
        self.world_up           = specs['world_up']
        self.yaw                = specs['yaw']
        self.pitch              = specs['pitch']
        self.movement_speed     = specs['speed']
        self.rotate_speed       = specs['rotate_speed']
        self.zoom               = specs['zoom']
        self.front_vec          = self.CalcFrontVec()
    def GetPos(self):
        # rotate along y axis
        cy = np.cos(self.yaw)
        sy = np.sin(self.yaw)
        Ry = np.array([[cy, 0, sy],[0, 1, 0],[-sy, 0, cy]])
        # rotate along x axis
        cx = np.cos(self.pitch)
        sx = np.sin(self.pitch)
        Rx = np.array([[1,0,0],[0, cx, -sx],[0, sx, cx]])
        pos = np.matmul(np.matmul(Rx, Ry), -self.position)
        pos = np.array([pos[1], pos[0], -pos[2]])
        return pos
    def GetPos_dep(self):
        # rotate along y axis
        cy = np.cos(self.yaw)
        sy = np.sin(self.yaw)
        Ry = np.array([[cy, 0, sy, 0],[0, 1, 0, 0],[-sy, 0, cy, 0],[0,0,0,1]])
        # rotate along x axis
        cx = np.cos(self.pitch)
        sx = np.sin(self.pitch)
        Rx = np.array([[1,0,0,0],[0, cx, -sx, 0],[0, sx, cx, 0],[0, 0, 0, 1]])
        # translate to self.position
        Tx = np.eye(4)
        Tx[0:3, 3] = self.position
        T = np.matmul(Tx, np.matmul(Rx, Ry))
        pos = np.array([-self.position[0], -self.position[1], -self.position[2], 1])
        return np.matmul(pos, T)[:3]
    def GetViewMatrix(self):
        # rotate along y axis
        cy = np.cos(self.yaw)
        sy = np.sin(self.yaw)
        Ry = np.array([[cy, 0, sy, 0],[0, 1, 0, 0],[-sy, 0, cy, 0],[0,0,0,1]])
        # rotate along x axis
        cx = np.cos(self.pitch)
        sx = np.sin(self.pitch)
        Rx = np.array([[1,0,0,0],[0, cx, -sx, 0],[0, sx, cx, 0],[0, 0, 0, 1]])
        # translate to self.position
        Tx = np.eye(4)
        Tx[0:3, 3] = self.position
        return np.matmul(Tx, np.matmul(Rx, Ry)).T
        #return np.matmul(Rx, np.matmul(Ry, Tx)).T
    def CalcFrontVec(self):
        """
        front_vec_x = np.cos(self.yaw)*np.cos(self.pitch)
        front_vec_y = np.sin(self.pitch)
        front_vec_z = np.sin(self.yaw)*np.cos(self.pitch)
        unormalized_front = np.array([front_vec_x, front_vec_y, front_vec_z])"""
        cy = np.cos(self.yaw)
        sy = np.sin(self.yaw)
        Ry = np.array([[cy, 0, sy, 0],[0, 1, 0, 0],[-sy, 0, cy, 0],[0,0,0,1]])
        # rotate along x axis
        cx = np.cos(self.pitch)
        sx = np.sin(self.pitch)
        Rx = np.array([[1,0,0,0],[0, cx, -sx, 0],[0, sx, cx, 0],[0, 0, 0, 1]])
        return Rx[0:3,2]
    def MoveCamera(self, movement_type, deltaT):
        #print(self.front_vec)
        if movement_type == 'forward':
            self.position += self.front_vec*self.movement_speed*deltaT
            return
        elif movement_type == 'backward':
            self.position -= self.front_vec*self.movement_speed*deltaT
            return
        elif movement_type == 'rotate_right':
            self.yaw -= self.rotate_speed*deltaT
        elif movement_type == 'rotate_left':
            self.yaw += self.rotate_speed*deltaT
        elif movement_type == 'rotate_up':
            self.pitch += self.rotate_speed*deltaT
        elif movement_type == 'rotate_down':
            self.pitch -= self.rotate_speed*deltaT
        self.front_vec = self.CalcFrontVec()
