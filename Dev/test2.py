import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.GL import shaders

#Initialize GLFW
if not glfw.init():
    raise Exception("GLFW could not be initialized!")

#Create a windowed mode window and its OpenGL context
window = glfw.create_window(800, 600, "Orthographic Projection", None, None)
if not window:
    glfw.terminate()
    raise Exception("GLFW window could not be created!")

glfw.make_context_current(window)

#Set up the orthographic projection matrix
glMatrixMode(GL_PROJECTION)
glLoadIdentity()

#Define the orthographic projection using glOrtho
sizew, sizeh = 800, 600  #Set your width and height for the window
glOrtho(0.0, sizew, sizeh, 0.0, -1.0, 1.0)  #Equivalent to gluOrtho2D

#Set the model view matrix
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

#Main loop
while not glfw.window_should_close(window):
    glClear(GL_COLOR_BUFFER_BIT)
    
    #Your rendering code here
    
    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()
