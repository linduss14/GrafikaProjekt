import pygame
from OpenGL.GL import *
import math

class Shockwave:
    def __init__(self):
        self.radius = 0.0
        self.active = False
        self.scale = 1.0

    def start(self, scale=1.0):
        self.active = True
        self.radius = 0.0
        self.scale = scale

    def update(self, dt):
        if self.active:
            self.radius += dt * 1.5 * self.scale 
            if self.radius > 6.0 * self.scale:
                self.active = False

    def draw(self):
        if not self.active:
            return
        glColor4f(0.8, 0.8, 0.8, 0.5) 
        glBegin(GL_LINE_LOOP)
        for i in range(64):
            angle = 2 * math.pi * i / 64
            x = self.radius * math.cos(angle)
            z = self.radius * math.sin(angle)
            glVertex3f(x, -0.6, z)
        glEnd()

    def reset(self):
        self.active = False
        self.radius = 0.0
        self.scale = 1.0
