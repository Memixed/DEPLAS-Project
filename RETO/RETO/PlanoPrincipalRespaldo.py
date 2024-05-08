import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
import numpy as np

screen_width = 900
screen_height = 600

#vc para el obser.
FOVY=60.0
ZNEAR=1.0
ZFAR=900.0

#Arreglo para el manejo de texturas
textures = []
filename1 = "RETO\piso.bmp"
filename2 = "RETO\cemento.bmp"
filename3 = "RETO\paredes.bmp"

#Variables para definir la posicion del observador
#gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
EYE_X = 300.0
EYE_Y = 200.0
EYE_Z = 300.0
CENTER_X = 0
CENTER_Y = 0
CENTER_Z = 0
UP_X=0
UP_Y=1
UP_Z=0

#Variables para dibujar los ejes del sistema
X_MIN=-500
X_MAX=500
Y_MIN=-500
Y_MAX=500
Z_MIN=-500
Z_MAX=500

#Dimension del plano
DimBoard = 200
DimBoardWidth = 192
DimBoardHeight = 230

#Variables para el control del observador
theta = 0.0
radius = 300

pygame.init()

def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    #X axis in red
    glColor3f(1.0,0.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN,0.0,0.0)
    glVertex3f(X_MAX,0.0,0.0)
    glEnd()
    #Y axis in green
    glColor3f(0.0,1.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,Y_MIN,0.0)
    glVertex3f(0.0,Y_MAX,0.0)
    glEnd()
    #Z axis in blue
    glColor3f(0.0,0.0,1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,0.0,Z_MIN)
    glVertex3f(0.0,0.0,Z_MAX)
    glEnd()
    glLineWidth(1.0)


def Init():
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: cubos")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

#Se mueve al observador circularmente al rededor del plano XZ a una altura fija (EYE_Y)
def lookat():
    global EYE_X
    global EYE_Z
    global radius
    EYE_X = radius * (math.cos(math.radians(theta)) + math.sin(math.radians(theta)))
    EYE_Z = radius * (-math.sin(math.radians(theta)) + math.cos(math.radians(theta)))
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    #glutPostRedisplay()

def Texturas(filepath):
    textures.append(glGenTextures(1))
    id = len(textures) - 1
    glBindTexture(GL_TEXTURE_2D, textures[id])
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    image = pygame.image.load(filepath).convert()
    w, h = image.get_rect().size
    image_data = pygame.image.tostring(image,"RGBA")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    glGenerateMipmap(GL_TEXTURE_2D) 

def PlanoTexturizado(distX1, distX2, distZ1, distZ2, textura):
    #Activate textures
    glColor3f(1.0,1.0,1.0)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures[textura])    
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(-(DimBoardWidth-distX1), 0, (DimBoardHeight-distZ1))
    glTexCoord2f(0.0, 1.0)
    glVertex3d(-(DimBoardWidth-distX1), 0, (DimBoardHeight-distZ2))
    glTexCoord2f(1.0, 1.0)
    glVertex3d(-(DimBoardWidth-distX2), 0, (DimBoardHeight-distZ2))
    glTexCoord2f(1.0, 0.0)
    glVertex3d(-(DimBoardWidth-distX2), 0, (DimBoardHeight-distZ1))
    glEnd()              
    glDisable(GL_TEXTURE_2D)

def drawFace(x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures[2])
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-(DimBoardWidth-x1), y1, (DimBoardHeight-z1))
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-(DimBoardWidth-x2), y2, (DimBoardHeight-z2))
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-(DimBoardWidth-x3), y3, (DimBoardHeight-z3))
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-(DimBoardWidth-x4), y4, (DimBoardHeight-z4))
    glEnd()
    glDisable(GL_TEXTURE_2D)

def Pared(texture, id):
    #Activate textures
    glEnable(GL_TEXTURE_2D)
    #front face
    glBindTexture(GL_TEXTURE_2D, texture[id])
    drawFace(-137, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0)
    #right face
    glBindTexture(GL_TEXTURE_2D, texture[id])
    drawFace(1.0, 1.0, 1.0, 1.0, -1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0)
    #back face
    glBindTexture(GL_TEXTURE_2D, texture[id])
    drawFace(1.0, 1.0, -1.0, -1.0, 1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, -1.0)
    #left face
    glBindTexture(GL_TEXTURE_2D, texture[id])
    drawFace(-1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, 1.0, 1.0)
    glDisable(GL_TEXTURE_2D)

def Plano():
    #Plano General
    glColor3f(0.9, 1.0, 0.7)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoardWidth, -2, -DimBoardHeight)
    glVertex3d(-DimBoardWidth, -2, DimBoardHeight)
    glVertex3d(DimBoardWidth, -2, DimBoardHeight)
    glVertex3d(DimBoardWidth, -2, -DimBoardHeight)
    glEnd() 

    #Pasillo 1
    PlanoTexturizado(0, 40, 0, 20, 0)
    
    #Pasillo 2
    PlanoTexturizado(20, 40, 20, 36, 0)

    #Pasillo 3
    PlanoTexturizado(20, 158, 36, 75.2, 0)

    #Pasillo 4
    PlanoTexturizado(142.6, 281.2, 36, 55.6, 0)

    #BODEGA 1 Pt.1
    PlanoTexturizado(142.6, 158, 75.2, 297.6, 1)

    #BODEGA 1 Pt.2
    PlanoTexturizado(158, 261.6, 55.6, 297.6, 1)
    
    #Pasillo 5
    PlanoTexturizado(261.2, 280.8, 36, 297.6, 0)

    #Pasillo 6
    PlanoTexturizado(280.8, 300.4, 281.6, 326, 0)

    #BODEGA 2
    PlanoTexturizado(209.6, 383.6, 326, 454.72, 1)

    #Drawface
    drawFace(137.6, 0, 75.2, 137.6, 10, 75.2, 137.6,10, 297.6, 137.6, 0, 297.6)
    drawFace(142.6, 0, 75.2, 142.6, 10, 75.2, 142.6,10, 297.6, 142.6, 0, 297.6)
    drawFace(137.6, 10, 75.2, 142.6, 10, 75.2, 142.6, 10, 297.6, 137.6, 10, 297.6)
    drawFace(137.6, 0, 75.2, 137.6, 10, 75.2, 142.6, 10, 75.2, 137.6, 0, 75.2)
    
    
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    Plano()
    #PlanoTexturizado()
    #Se dibuja cubos
    
done = False

Init()

while not done:
    keys = pygame.key.get_pressed()
    #avanzar observador
    if keys[pygame.K_RIGHT]:
        if theta > 359.0:
            theta = 0
        else:
            theta += 1.0
        lookat()        
    if keys[pygame.K_LEFT]:
        if theta < 1.0:
            theta = 360.0
        else:
            theta += -1.0
        lookat()        

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True

    Texturas(filename1)
    Texturas(filename2)
    Texturas(filename3)

    display()

    pygame.display.flip()
    pygame.time.wait(5)

pygame.quit()