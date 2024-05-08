import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import pandas as pd

import math
import numpy as np

from objloader import *

screen_width = 900
screen_height = 600

#vc para el obser.
FOVY=60.0
ZNEAR=1.0
ZFAR=900.0

#Manejo de texturas
textures = []
filename1 = "piso.bmp"
filename2 = "cemento.bmp"
filename3 = "paredesB.bmp"

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

#Coordenadas del sistema
coord=pd.read_csv("coordZonas.csv")
coordP = pd.read_csv("paredes.csv")
objetosCSV = pd.read_csv("objetosCSV.csv")

#Variables para el control del observador
theta = 0.0
radius = 300

objetos = []

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

    """
    objetos.append(OBJ("RETO/monta.obj", swapyz=True))
    objetos[0].generate()
    
    objetos.append(OBJ("RETO/tarimas.obj", swapyz=True))
    objetos[0].generate()
    """
    objetos.append(OBJ("saco.obj", swapyz=True))
    objetos[0].generate()
    
    objetos.append(OBJ("oficinas.obj", swapyz=True))
    objetos[1].generate()
    
    objetos.append(OBJ("bodega.obj", swapyz=True))
    objetos[2].generate() #cambiar a 4

    objetos.append(OBJ("bascula.obj", swapyz=True))
    objetos[3].generate() #cambiar a 4

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

def nuevoMuro(pix, piz, y, w, h):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures[2])

    x = -(DimBoardWidth-pix)
    z = (DimBoardHeight-piz)

    #MURO A
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(x, 0, z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(x, y, z)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(x, y, (z-h))
    glTexCoord2f(1.0, 0.0)
    glVertex3f(x, 0, (z-h))
    glEnd()

    #MURO B
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f((x+w), 0, z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f((x+w), y, z)
    glTexCoord2f(1.0, 1.0)
    glVertex3f((x+w), y, (z-h))
    glTexCoord2f(1.0, 0.0)
    glVertex3f((x+w), 0, (z-h))
    glEnd()

    #MURO C
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(x, y, z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(x, y, (z-h))
    glTexCoord2f(1.0, 1.0)
    glVertex3f((x+w), y, (z-h))
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
    glVertex3f(x, 0, (z-h))
    glTexCoord2f(0.0, 1.0)
    glVertex3f(x, y, (z-h))
    glTexCoord2f(1.0, 1.0)
    glVertex3f((x+w), y, (z-h))
    glTexCoord2f(1.0, 0.0)
    glVertex3f((x+w), 0, (z-h))
    glEnd()


    glDisable(GL_TEXTURE_2D)

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

def Texturas(filepath):
    textures.append(glGenTextures(1))
    id = len(textures) - 1
    glBindTexture(GL_TEXTURE_2D, textures[id])
    #glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S, GL_CLAMP)
    #glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    image = pygame.image.load(filepath).convert()
    w, h = image.get_rect().size
    image_data = pygame.image.tostring(image,"RGBA")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    glGenerateMipmap(GL_TEXTURE_2D) 
    
def Plano():
    #Plano General
    glColor3f(0.9, 1.0, 0.7)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoardWidth, -2, -DimBoardHeight)
    glVertex3d(-DimBoardWidth, -2, DimBoardHeight)
    glVertex3d(DimBoardWidth, -2, DimBoardHeight)
    glVertex3d(DimBoardWidth, -2, -DimBoardHeight)
    glEnd() 

    #Pasillos
    #Zona.LeerZonas("RETO\coordZonas.csv")

def displayobj(x, z, e, o, g):
    
    glPushMatrix()  
    # Ajustes para la posición y orientación del objeto
    glTranslatef(-(DimBoardWidth-x), 0.0, (DimBoardHeight-z) )  # Ajuste de traslación para posicionarlo en el plano
    glRotatef(g, 0.0, 1.0, 0.0)  # Rotación para que el objeto mire hacia arriba
    # Escala del objeto para hacerlo más visible
    glScalef(e, e, e)  # Escala el objeto para que sea más grande
    objetos[o].render()
    glPopMatrix()
    
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    Plano()

    #displayobj()

    for i in range(len(coord)):
        PlanoTexturizado(coord["distX"][i], coord["distX1"][i], coord["distZ"][i], coord["distZ1"][i], coord["textura"][i])
    
    for j in range(len(coordP)):
        nuevoMuro(coordP["pix"][j], coordP["piz"][j], coordP["y"][j], coordP["w"][j], coordP["h"][j])

    for k in range(len(objetosCSV)):
        displayobj(objetosCSV["x"][k], objetosCSV["z"][k], objetosCSV["esc"][k], objetosCSV["objeto"][k], objetosCSV["g"][k])

    
done = False

Init()

Texturas(filename1)
Texturas(filename2)
Texturas(filename3)

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

    display()

    pygame.display.flip()
    pygame.time.wait(5)

pygame.quit()