import pygame
from OpenGL.GL import *
from config import GROUND_LEVEL

def load_obj(filename):
    vertices = []
    faces = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.split('#')[0].strip()
                if not line:
                    continue
                if line.startswith('v '):
                    parts = line.split()
                    vertices.append((float(parts[1]), float(parts[2]), float(parts[3])))
                elif line.startswith('f '):
                    parts = line.split()
                    face = [int(p.split('/')[0]) - 1 for p in parts[1:]]
                    faces.append(face)
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku {filename}")
        return [], []
    except Exception as e:
        print(f"Błąd podczas wczytywania pliku {filename}: {e}")
        return [], []
    return vertices, faces

class Bomb:
    def __init__(self):
        self.x = 0.0
        self.y = 1.2
        self.z = 0.0
        self.speed = 1.0
        self.exploded = False
        self.vertices, self.faces = load_obj("bomb.obj")
        if not self.vertices or not self.faces:
            print("Nie udało się wczytać modelu bomby. Używanie domyślnego punktu.")
            self.model_loaded = False
        else:
            self.model_loaded = True

    def update(self, dt):
        if not self.exploded:
            self.y -= self.speed * dt
            if self.y <= GROUND_LEVEL:
                self.y = GROUND_LEVEL
                self.exploded = True

    def draw(self, scale=1.0):
        if self.exploded:
            return
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glRotatef(180, 1, 0, 0)
        glScalef(scale, scale, scale)
        if self.model_loaded:
            glColor3f(0.2, 0.2, 0.2)
            for face in self.faces:
                if len(face) == 3:
                    glBegin(GL_TRIANGLES)
                elif len(face) == 4:
                    glBegin(GL_QUADS)
                else:
                    glBegin(GL_POLYGON)
                for vertex_index in face:
                    if 0 <= vertex_index < len(self.vertices):
                        glVertex3fv(self.vertices[vertex_index])
                    else:
                        pass
                glEnd()
        else:
            glColor3f(1.0, 0.3, 0.0)
            glPointSize(24 * scale)
            glVertex3f(0,0,0)
            glEnd()
        glPopMatrix()

    def reset(self):
        self.x = 0.0
        self.y = 1.2
        self.z = 0.0
        self.exploded = False
