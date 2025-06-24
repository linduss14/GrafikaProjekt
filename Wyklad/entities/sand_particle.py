import pygame
from OpenGL.GL import *
import random
import math
from config import (
    GROUND_LEVEL,
    DEFAULT_SAND_SPEED_MIN, DEFAULT_SAND_SPEED_MAX,
    DEFAULT_SAND_GRAVITY_MULTIPLIER,
    DEFAULT_SAND_LIFE_MIN, DEFAULT_SAND_LIFE_MAX
)

class SandParticle:
    def __init__(self, initial_explosion_scale=1.0, params=None):
        self.active = False
        self.explosion_scale = initial_explosion_scale
        self.params = params if params else {}
        self.reset()

    def reset(self):
        self.x = 0.0
        self.y = GROUND_LEVEL + random.uniform(0.05, 0.15) * self.explosion_scale
        self.z = 0.0
        
        angle_horizontal = random.uniform(0, 2 * math.pi)
        angle_vertical = random.uniform(math.pi / 6, math.pi / 3)
        speed_min = self.params.get('sand_speed_min', DEFAULT_SAND_SPEED_MIN)
        speed_max = self.params.get('sand_speed_max', DEFAULT_SAND_SPEED_MAX)
        speed = random.uniform(speed_min, speed_max) * self.explosion_scale 
        
        self.vx = speed * math.cos(angle_horizontal) * math.sin(angle_vertical)
        self.vz = speed * math.sin(angle_horizontal) * math.sin(angle_vertical)
        self.vy = speed * math.cos(angle_vertical)
        
        self.size = random.uniform(2, 5)
        life_min = self.params.get('sand_life_min', DEFAULT_SAND_LIFE_MIN)
        life_max = self.params.get('sand_life_max', DEFAULT_SAND_LIFE_MAX)
        self.life = random.uniform(life_min, life_max)
        self.age = 0.0
        self.active = False
        r = random.uniform(0.6, 0.8)
        g = random.uniform(0.5, 0.7)
        b = random.uniform(0.3, 0.5)
        self.color = (r, g, b)
        gravity_multiplier = self.params.get('sand_gravity_multiplier', DEFAULT_SAND_GRAVITY_MULTIPLIER)
        self.gravity = 9.8 * gravity_multiplier * self.explosion_scale

    def activate(self):
        self.x = 0.0 
        self.y = GROUND_LEVEL + random.uniform(0.05, 0.15) * self.explosion_scale
        self.z = 0.0
        angle_horizontal = random.uniform(0, 2 * math.pi)
        angle_vertical = random.uniform(math.pi / 6, math.pi / 3)
        speed_min = self.params.get('sand_speed_min', DEFAULT_SAND_SPEED_MIN)
        speed_max = self.params.get('sand_speed_max', DEFAULT_SAND_SPEED_MAX)
        speed = random.uniform(speed_min, speed_max) * self.explosion_scale 
        self.vx = speed * math.cos(angle_horizontal) * math.sin(angle_vertical)
        self.vz = speed * math.sin(angle_horizontal) * math.sin(angle_vertical)
        self.vy = speed * math.cos(angle_vertical)
        life_min = self.params.get('sand_life_min', DEFAULT_SAND_LIFE_MIN)
        life_max = self.params.get('sand_life_max', DEFAULT_SAND_LIFE_MAX)
        self.life = random.uniform(life_min, life_max)
        self.age = 0.0
        self.active = True
        gravity_multiplier = self.params.get('sand_gravity_multiplier', DEFAULT_SAND_GRAVITY_MULTIPLIER)
        self.gravity = 9.8 * gravity_multiplier * self.explosion_scale

    def update(self, dt):
        if not self.active:
            return
        self.age += dt
        self.vy -= self.gravity * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.z += self.vz * dt
        self.life -= dt
        if self.life <= 0 or self.y < GROUND_LEVEL - 0.1:
            self.active = False
            self.reset()

    def draw(self):
        if not self.active:
            return
        alpha = max(0.0, min(1.0, self.life * 2.0))
        glColor4f(self.color[0], self.color[1], self.color[2], alpha)
        glPointSize(self.size * self.explosion_scale**0.5)
        glBegin(GL_POINTS)
        glVertex3f(self.x, self.y, self.z)
        glEnd()
