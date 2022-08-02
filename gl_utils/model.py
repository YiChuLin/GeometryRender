import os
import numpy as np
from OpenGL.GL import *
from ctypes import c_void_p
from PIL import Image
from tqdm import tqdm

class Model():
    """
    Currently Reads an obj file that contains vertices(v), vertex normals (vn), and faces. All other
    attributes will be ignored. (In the future we should add the texture reading function)
    """
    def __init__(self, obj_filepath):
        assert(os.path.isfile(obj_filepath)), "Input file \"" + obj_filepath + "\" doesn't exist."
        if obj_filepath[-4:] != '.obj':
            print('Warning, the provided file is not an obj file, trying to process it anyway')
        self.vertices = []
        self.indices = []
        # process file
        self.ProcessFile(obj_filepath)
        # Now set up for drawing
        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        self.EBO = glGenBuffers(1)
        self.SetUp()

    def Draw(self, shader, width = 400, height = 400):
        """
        the input shader is currently not used since we don't have texture
        """
        glBindVertexArray(self.VAO)
        #glViewport(0, 0, width, height)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

    def SetUp(self):
        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)
        position = 0 #glGetAttribLocation(shaderProgram, 'aPos')
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 6*ctypes.sizeof(GLfloat), None)
        glEnableVertexAttribArray(position)
        normal = 1
        glVertexAttribPointer(normal, 3, GL_FLOAT, GL_FALSE, 6*ctypes.sizeof(GLfloat), c_void_p(3*ctypes.sizeof(GLfloat)))
        glEnableVertexAttribArray(normal)
        glBindVertexArray(0)
    def ProcessFile(self, obj_filepath):
        position = []
        normal = []
        print("loading obj...")
        with open(obj_filepath, 'r') as f:
            for line in tqdm(f):
                # get rid of comments
                #print(line)
                line = line[:line.find('#')]
                components = line.split()
                if len(components) == 4:
                    #Valid split
                    if components[0] == 'v':
                        #vertex
                        vertex = [float(c) for c in components[1:]]
                        #vertex[0] = vertex[0] - 0.02
                        position.append(vertex)
                    elif components[0] == 'vn':
                        #normal
                        normal.append([float(c) for c in components[1:]])
                    elif components[0] == 'f':
                        #faces
                        for face in components[1:]:
                            comp = face.split('/')
                            # assume pos_index = norm_index
                            pos_index = int(comp[0]) - 1
                            norm_index = int(comp[-1]) - 1 #in case there are texture components we are ignoring
                            self.indices.append(pos_index)
        self.position = np.array(position)
        self.normal = np.array(normal)
        for v, vn in tqdm(zip(position, normal)):
            self.vertices.extend(v)
            self.vertices.extend(vn)
        self.vertices = np.array(self.vertices, dtype=np.float32)
        self.indices = np.array(self.indices, dtype=np.uintc)