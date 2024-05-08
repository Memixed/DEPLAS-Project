import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import pandas as pd

import math
import numpy as np

#Dimension del plano
DimBoard = 200
DimBoardWidth = 192
DimBoardHeight = 230

textures=[]


def nuevoMuro(pix, piz, y, w, h):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures[2])

    x = -(DimBoardWidth-pix)
    z = (DimBoardWidth-piz)

    #MURO A
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(x, 0, z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(x, y, z)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(x, y, (z+h))
    glTexCoord2f(1.0, 0.0)
    glVertex3f(x, 0, (z+h))
    glEnd()

    #MURO B
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f((x+w), 0, z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f((x+w), y, z)
    glTexCoord2f(1.0, 1.0)
    glVertex3f((x+w), y, (z+h))
    glTexCoord2f(1.0, 0.0)
    glVertex3f((x+w), 0, (z+h))
    glEnd()

    #MURO C
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(x, y, z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(x, y, (z+h))
    glTexCoord2f(1.0, 1.0)
    glVertex3f((x+w), y, (z+h))
    glTexCoord2f(1.0, 0.0)
    glVertex3f((x+w), y, z)
    glEnd()

    #MURO D
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(x, 0, z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(x, y, z)
    glTexCoord2f(1.0, 1.0)
    glVertex3f((x+w), y, z)
    glTexCoord2f(1.0, 0.0)
    glVertex3f((x+w), 0, z)
    glEnd()

    #MURO E
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(x, 0, (z+h))
    glTexCoord2f(0.0, 1.0)
    glVertex3f(x, y, (z+h))
    glTexCoord2f(1.0, 1.0)
    glVertex3f((x+w), y, (z+h))
    glTexCoord2f(1.0, 0.0)
    glVertex3f((x+w), 0, (z+h))
    glEnd()


    glDisable(GL_TEXTURE_2D)