import pygame
from OpenGL.GL import *
import random
import math
from config import (
    GROUND_LEVEL, 
    DEFAULT_CLOUD_SPREAD_SPEED_MIN, DEFAULT_CLOUD_SPREAD_SPEED_MAX,
    DEFAULT_CLOUD_INITIAL_LIFT_MIN, DEFAULT_CLOUD_INITIAL_LIFT_MAX,
    DEFAULT_CLOUD_AIR_RESISTANCE, DEFAULT_CLOUD_GRAVITY,
    DEFAULT_PARTICLE_LIFE_MULTIPLIER
)

class Particle:
    def __init__(self, initial_explosion_scale=1.0, params=None):
        self.active = False
        self.explosion_scale = initial_explosion_scale
        self.params = params if params else {}
        self.reset() 

    def reset(self):
        self.phase = "stem"
        self.x = 0.0
        self.y = GROUND_LEVEL 
        self.z = 0.0
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(0.0, 0.2) * self.explosion_scale 
        self.vx = radius * math.cos(angle)
        self.vz = radius * math.sin(angle)
        self.vy = random.uniform(1.0, 1.3) * self.explosion_scale 
        self.size = random.uniform(12, 20)
        particle_life_multiplier = self.params.get('particle_life_multiplier', DEFAULT_PARTICLE_LIFE_MULTIPLIER)
        self.life = 1.5 + (self.explosion_scale - 1.0) * (particle_life_multiplier / 2.0)
        self.age = 0.0
        self.active = False

    def activate(self):
        self.phase = "stem"
        self.x = 0.0 
        self.y = GROUND_LEVEL
        self.z = 0.0
        
        angle_stem = random.uniform(0, 2 * math.pi)
        radius_stem = random.uniform(0.005, 0.02) * self.explosion_scale
        self.vx = radius_stem * math.cos(angle_stem)
        self.vz = radius_stem * math.sin(angle_stem)
        self.vy = random.uniform(1.5, 2.0) * self.explosion_scale
        
        self.size = random.uniform(12, 20) 
        particle_life_multiplier = self.params.get('particle_life_multiplier', DEFAULT_PARTICLE_LIFE_MULTIPLIER)
        self.life = 4.0 + (self.explosion_scale - 1.0) * particle_life_multiplier 
        self.age = 0.0
        self.active = True

    def update(self, dt):
        if not self.active:
            return
        self.age += dt

        if self.phase == "stem":
            self.y += self.vy * dt
            self.x += self.vx * dt 
            self.z += self.vz * dt 
            self.vy -= 0.8 * dt * self.explosion_scale

            if self.vy <= 0.01 * self.explosion_scale:
                self.phase = "cloud"
                cloud_spread_angle = random.uniform(0, 2 * math.pi)
                spread_min = self.params.get('cloud_spread_speed_min', DEFAULT_CLOUD_SPREAD_SPEED_MIN)
                spread_max = self.params.get('cloud_spread_speed_max', DEFAULT_CLOUD_SPREAD_SPEED_MAX)
                cloud_spread_speed = random.uniform(spread_min, spread_max) * self.explosion_scale 
                self.vx = cloud_spread_speed * math.cos(cloud_spread_angle)
                self.vz = cloud_spread_speed * math.sin(cloud_spread_angle)
                lift_min = self.params.get('cloud_initial_lift_min', DEFAULT_CLOUD_INITIAL_LIFT_MIN)
                lift_max = self.params.get('cloud_initial_lift_max', DEFAULT_CLOUD_INITIAL_LIFT_MAX)
                self.vy = random.uniform(lift_min, lift_max) * self.explosion_scale

        elif self.phase == "cloud":
            self.x += self.vx * dt
            self.y += self.vy * dt
            self.z += self.vz * dt
            
            cloud_gravity = self.params.get('cloud_gravity', DEFAULT_CLOUD_GRAVITY)
            self.vy -= cloud_gravity * dt * self.explosion_scale 
            
            air_resistance = self.params.get('cloud_air_resistance', DEFAULT_CLOUD_AIR_RESISTANCE)
            self.vx *= (1 - air_resistance * dt) 
            self.vz *= (1 - air_resistance * dt)

        self.life -= dt
        if self.life <= 0 or self.y < GROUND_LEVEL - 0.2: 
            self.active = False

    def draw(self):
        if not self.active:
            return
        
        if self.phase == "stem":
            glColor3f(0.6, 0.6, 0.6)
        else:
            glColor3f(0.5, 0.5, 0.5)

        draw_size = self.size * (self.explosion_scale**0.5) 
        draw_size = min(draw_size, 40.0)
        glPointSize(max(1.0, draw_size))
        glBegin(GL_POINTS)
        glVertex3f(self.x, self.y, self.z)
        glEnd()
