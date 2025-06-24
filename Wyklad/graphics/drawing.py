from OpenGL.GL import *
from OpenGL.GLU import *
import math
from config import GROUND_LEVEL

def draw_crater(depth=0.3, radius=0.6, segments=32, center_x=0.0, center_z=0.0):
    bottom_color = (0.0, 0.0, 0.0)
    edge_color = (0.5, 0.35, 0.2)

    bottom_vertices = []
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        x = center_x + radius * 0.6 * math.cos(angle)
        z = center_z + radius * 0.6 * math.sin(angle)
        bottom_vertices.append((x, GROUND_LEVEL - depth, z))

    edge_vertices = []
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        x = center_x + radius * math.cos(angle)
        z = center_z + radius * math.sin(angle)
        edge_vertices.append((x, GROUND_LEVEL, z))

    glColor3fv(bottom_color)
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(center_x, GROUND_LEVEL - depth, center_z)
    for i in range(segments + 1):
        vx, vy, vz = bottom_vertices[i % segments]
        glVertex3f(vx, vy, vz)
    glEnd()

    glBegin(GL_TRIANGLE_STRIP)
    for i in range(segments + 1):
        bx, by, bz = bottom_vertices[i % segments]
        ex, ey, ez = edge_vertices[i % segments]
        
        glColor3fv(bottom_color)
        glVertex3f(bx, by, bz) 
        
        glColor3fv(edge_color)
        glVertex3f(ex, ey, ez)
    glEnd()

def draw_ground(crater_present=False, crater_radius=0.6, crater_center_x=0.0, crater_center_z=0.0, extent=10.0):
    y_level = GROUND_LEVEL - 0.01
    glColor3f(0.94, 0.86, 0.6)

    if not crater_present:
        glBegin(GL_QUADS)
        glVertex3f(-extent, y_level, -extent)
        glVertex3f(extent, y_level, -extent)
        glVertex3f(extent, y_level, extent)
        glVertex3f(-extent, y_level, extent)
        glEnd()
    else:
        glEnable(GL_STENCIL_TEST)
        glStencilFunc(GL_ALWAYS, 1, 0xFF) 
        glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE) 

        glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE)
        glDepthMask(GL_FALSE)

        glPushMatrix()
        glTranslatef(crater_center_x, y_level, crater_center_z) 
        glRotatef(-90, 1, 0, 0)
        quad = gluNewQuadric()
        gluDisk(quad, 0, crater_radius, 32, 1) 
        gluDeleteQuadric(quad)
        glPopMatrix()

        glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE)
        glDepthMask(GL_TRUE)

        glStencilFunc(GL_NOTEQUAL, 1, 0xFF) 
        glStencilOp(GL_KEEP, GL_KEEP, GL_KEEP)   

        glBegin(GL_QUADS)
        glVertex3f(-extent, y_level, -extent)
        glVertex3f(extent, y_level, -extent)
        glVertex3f(extent, y_level, extent)
        glVertex3f(-extent, y_level, extent)
        glEnd()

        glDisable(GL_STENCIL_TEST)

def draw_background_sides():
    glColor3f(0.7, 0.85, 1.0)
    height = 5.0
    size = 10.0
    glBegin(GL_QUADS)
    glVertex3f(-size, GROUND_LEVEL - 0.01, size)
    glVertex3f(size, GROUND_LEVEL - 0.01, size)
    glVertex3f(size, height, size)
    glVertex3f(-size, height, size)
    glVertex3f(-size, GROUND_LEVEL - 0.01, -size)
    glVertex3f(size, GROUND_LEVEL - 0.01, -size)
    glVertex3f(size, height, -size)
    glVertex3f(-size, height, -size)
    glVertex3f(-size, GROUND_LEVEL - 0.01, -size)
    glVertex3f(-size, GROUND_LEVEL - 0.01, size)
    glVertex3f(-size, height, size)
    glVertex3f(-size, height, -size)
    glVertex3f(size, GROUND_LEVEL - 0.01, -size)
    glVertex3f(size, GROUND_LEVEL - 0.01, size)
    glVertex3f(size, height, size)
    glVertex3f(size, height, -size)
    glEnd()
