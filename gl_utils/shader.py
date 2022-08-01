from OpenGL.GL import *
from OpenGL.GL import shaders
import numpy as np
import os

strShader = {
    GL_VERTEX_SHADER:"vertex",
    GL_GEOMETRY_SHADER:"geometry",
    GL_FRAGMENT_SHADER:"fragment"
}

class Shader():
    def __init__(self, v_shader_path, f_shader_path):
        vShader = self.createShader(v_shader_path, GL_VERTEX_SHADER)
        fShader = self.createShader(f_shader_path, GL_FRAGMENT_SHADER)
        self.program = self.createProgram([vShader, fShader])
    def use(self):
        glUseProgram(self.program)
    def setFloat(self, var_name, val):
        glUniform1f(glGetUniformLocation(self.program, var_name), val)
    def setInt(self, var_name, val):
        glUniform1i(glGetUniformLocation(self.program, var_name), val)
    def setVec(self, var_name, vec):
        if not isinstance(vec, np.ndarray):
            vec = np.array(vec)
        assert(len(vec.shape) == 1), "Error in setting vector, vector must be 1 dimension, instead got shape" + vec.shape
        if vec.shape[0] == 2:
            glUniform2fv(glGetUniformLocation(self.program, var_name), 1, vec)
        elif vec.shape[0] == 3:
            glUniform3fv(glGetUniformLocation(self.program, var_name), 1, vec)
        elif vec.shape[0] == 4:
            glUniform4fv(glGetUniformLocation(self.program, var_name), 1, vec)
        else:
            print("Cannot set vector, please ensure the size of the vecotr is either 2, 3, or 4")
    def setMat(self, var_name, mat):
        if not isinstance(mat, np.ndarray):
            mat = np.array(mat)
        assert(len(mat.shape) == 2 and mat.shape[0] == mat.shape[1]), "Error, Matrix Shape Mismatch"
        if mat.shape[0] == 2:
            glUniformMatrix2fv(glGetUniformLocation(self.program, var_name), 1, GL_FALSE, mat)
        elif mat.shape[0] == 3:
            glUniformMatrix3fv(glGetUniformLocation(self.program, var_name), 1, GL_FALSE, mat)
        elif mat.shape[0] == 4:
            glUniformMatrix4fv(glGetUniformLocation(self.program, var_name), 1, GL_FALSE, mat)
        else:
            print("Cannot set matrix, please ensure the size of the matrix is either 2, 3, or 4")
    def GetAttribLocation(self, var_name):
        return glGetAttribLocation(self.program, var_name)
    def createShader(self, shader_path, shaderType):
        assert(os.path.isfile(shader_path)), "Cannot find " + shader_path
        assert(shaderType is GL_VERTEX_SHADER or shaderType is GL_FRAGMENT_SHADER or shaderType is GL_GEOMETRY_SHADER), "Invalid Shader Type"
        shader_glsl = open(shader_path, 'r').readlines()
        #shader = shaders.compileShader(shader_glsl, shaderType)
        shader = glCreateShader(shaderType)
        glShaderSource(shader, shader_glsl)
        glCompileShader(shader)
        # Check if succesfully compiled
        status = glGetShaderiv(shader, GL_COMPILE_STATUS)
        if status == GL_FALSE:
            InfoLog = glGetShaderInfoLog(shader)
            print("Compilation failure for {} shader:\n".format(strShader[shaderType]) + str(InfoLog))
        return shader
    def createProgram(self, shader_list):
        program = glCreateProgram()
        for shader in shader_list:
            glAttachShader(program, shader)
        glLinkProgram(program)
        #Check for errors
        status = glGetProgramiv(program, GL_LINK_STATUS)
        if status == GL_FALSE:
            InfoLog = glGetProgramInfoLog(program)
            print("Linker failure: \n" + str(InfoLog))
        # Noe detech the shaders since they are no longer needed
        for shader in shader_list:
            glDetachShader(program, shader)
        return program
