import pygame
import pygame_gui
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math
import json

from config import (
    WIDTH, HEIGHT, NUM_PARTICLES, NUM_SAND_PARTICLES, SETTINGS_FILE,
    DEFAULT_CLOUD_SPREAD_SPEED_MIN, DEFAULT_CLOUD_SPREAD_SPEED_MAX,
    DEFAULT_CLOUD_INITIAL_LIFT_MIN, DEFAULT_CLOUD_INITIAL_LIFT_MAX,
    DEFAULT_CLOUD_AIR_RESISTANCE, DEFAULT_CLOUD_GRAVITY,
    DEFAULT_PARTICLE_LIFE_MULTIPLIER,
    DEFAULT_SAND_SPEED_MIN, DEFAULT_SAND_SPEED_MAX,
    DEFAULT_SAND_GRAVITY_MULTIPLIER,
    DEFAULT_SAND_LIFE_MIN, DEFAULT_SAND_LIFE_MAX
)
DEFAULT_BOMB_VISUAL_SCALE = 0.5 

from entities.bomb import Bomb
from entities.particle import Particle
from entities.sand_particle import SandParticle
from entities.shockwave import Shockwave
from graphics.drawing import draw_crater, draw_ground, draw_background_sides

global_explosion_scale = 1.0
DEFAULT_EXPLOSION_SCALE = 1.0
particles_activated_this_explosion = False
current_settings = {}

def load_settings():
    global current_settings
    default_settings = {
        'explosion_scale': DEFAULT_EXPLOSION_SCALE,
        'cloud_spread_speed_min': DEFAULT_CLOUD_SPREAD_SPEED_MIN,
        'cloud_spread_speed_max': DEFAULT_CLOUD_SPREAD_SPEED_MAX,
        'cloud_initial_lift_min': DEFAULT_CLOUD_INITIAL_LIFT_MIN,
        'cloud_initial_lift_max': DEFAULT_CLOUD_INITIAL_LIFT_MAX,
        'cloud_air_resistance': DEFAULT_CLOUD_AIR_RESISTANCE,
        'cloud_gravity': DEFAULT_CLOUD_GRAVITY,
        'particle_life_multiplier': DEFAULT_PARTICLE_LIFE_MULTIPLIER,
        'sand_speed_min': DEFAULT_SAND_SPEED_MIN,
        'sand_speed_max': DEFAULT_SAND_SPEED_MAX,
        'sand_gravity_multiplier': DEFAULT_SAND_GRAVITY_MULTIPLIER,
        'sand_life_min': DEFAULT_SAND_LIFE_MIN,
        'sand_life_max': DEFAULT_SAND_LIFE_MAX,
        'bomb_visual_scale': DEFAULT_BOMB_VISUAL_SCALE,
    }
    current_settings = default_settings.copy()
    try:
        with open(SETTINGS_FILE, 'r') as f:
            loaded_settings_from_file = json.load(f)
            current_settings.update(loaded_settings_from_file)
    except FileNotFoundError:
        print(f"Plik {SETTINGS_FILE} nie znaleziony. Używam wartości domyślnych.")
    except json.JSONDecodeError:
        print(f"Błąd odczytu pliku {SETTINGS_FILE}. Używam wartości domyślnych.")
    except Exception as e:
        print(f"Inny błąd podczas wczytywania ustawień: {e}. Używam wartości domyślnych.")

def save_settings(scale_slider=None):
    global current_settings, global_explosion_scale
    if scale_slider is not None:
        current_settings['explosion_scale'] = scale_slider.get_current_value()
        global_explosion_scale = current_settings['explosion_scale']
    else:
        current_settings['explosion_scale'] = global_explosion_scale
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(current_settings, f, indent=4)
    except IOError:
        print(f"Nie udało się zapisać ustawień do pliku {SETTINGS_FILE}")

def reset_simulation(bomb, particles, sand_particles, shockwave, scale_slider=None, scale_label=None):
    global global_explosion_scale, sand_shot_this_explosion, particles_activated_this_explosion, current_settings
    bomb.reset()
    global_explosion_scale = current_settings.get('explosion_scale', DEFAULT_EXPLOSION_SCALE)
    if scale_slider is not None:
        scale_slider.set_current_value(global_explosion_scale)
    if scale_label is not None:
        scale_label.set_text(f'Skala eksplozji: {global_explosion_scale:.2f}')
    for p in particles:
        p.explosion_scale = global_explosion_scale
        p.params = current_settings
        p.reset()
    for sp in sand_particles:
        sp.explosion_scale = global_explosion_scale
        sp.params = current_settings
        sp.reset()
    shockwave.reset()
    sand_shot_this_explosion = False
    particles_activated_this_explosion = False

def main():
    global global_explosion_scale, sand_shot_this_explosion, particles_activated_this_explosion, current_settings
    load_settings()
    global_explosion_scale = current_settings.get('explosion_scale', DEFAULT_EXPLOSION_SCALE)
    sand_shot_this_explosion = False
    particles_activated_this_explosion = False 
    pygame.init()
    pygame.display.gl_set_attribute(pygame.GL_STENCIL_SIZE, 8)
    screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Mushroom Cloud 3D")
    gui_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    scene_width = int(WIDTH * 0.7)
    menu_width = WIDTH - scene_width
    menu_x_start = scene_width
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    y_offset = 10
    label_height = 30
    slider_height = 30
    button_height = 40
    spacing = 5
    scale_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((menu_x_start + 10, y_offset), (menu_width - 20, label_height)),
        text=f'Skala eksplozji: {global_explosion_scale:.2f}', manager=manager
    )
    y_offset += label_height + spacing
    scale_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((menu_x_start + 10, y_offset), (menu_width - 20, slider_height)),
        start_value=global_explosion_scale, value_range=(0.1, 5.0), manager=manager
    )
    y_offset += slider_height + spacing * 2
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((menu_x_start + 10, y_offset), (menu_width - 20, label_height)),
        text='Parametry Chmury:', manager=manager, object_id='#section_header'
    )
    y_offset += label_height + spacing
    cloud_spread_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((menu_x_start + 10, y_offset), (menu_width - 20, label_height)),
        text=f"Rozrzut: {current_settings['cloud_spread_speed_min']:.2f}-{current_settings['cloud_spread_speed_max']:.2f}", manager=manager
    )
    y_offset += label_height + spacing
    cloud_spread_min_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((menu_x_start + 10, y_offset), (menu_width - 20, slider_height)),
        start_value=current_settings['cloud_spread_speed_min'], value_range=(0.1, 5.0), manager=manager
    )
    y_offset += slider_height + spacing
    cloud_spread_max_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((menu_x_start + 10, y_offset), (menu_width - 20, slider_height)),
        start_value=current_settings['cloud_spread_speed_max'], value_range=(0.1, 5.0), manager=manager
    )
    y_offset += slider_height + spacing
    cloud_air_resistance_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((menu_x_start + 10, y_offset), (menu_width - 20, label_height)),
        text=f"Opór pow. chmury: {current_settings['cloud_air_resistance']:.4f}", manager=manager
    )
    y_offset += label_height + spacing
    cloud_air_resistance_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((menu_x_start + 10, y_offset), (menu_width - 20, slider_height)),
        start_value=current_settings['cloud_air_resistance'], value_range=(0.0001, 0.1), manager=manager
    )
    y_offset += slider_height + spacing * 2
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((menu_x_start + 10, y_offset), (menu_width - 20, label_height)),
        text='Parametry Piasku:', manager=manager, object_id='#section_header'
    )
    y_offset += label_height + spacing
    sand_speed_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((menu_x_start + 10, y_offset), (menu_width - 20, label_height)),
        text=f"Prędkość piasku: {current_settings['sand_speed_min']:.2f}-{current_settings['sand_speed_max']:.2f}", manager=manager
    )
    y_offset += label_height + spacing
    sand_speed_min_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((menu_x_start + 10, y_offset), (menu_width - 20, slider_height)),
        start_value=current_settings['sand_speed_min'], value_range=(0.1, 5.0), manager=manager
    )
    y_offset += slider_height + spacing
    sand_speed_max_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((menu_x_start + 10, y_offset), (menu_width - 20, slider_height)),
        start_value=current_settings['sand_speed_max'], value_range=(0.1, 5.0), manager=manager
    )
    y_offset += slider_height + spacing
    sand_gravity_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((menu_x_start + 10, y_offset), (menu_width - 20, label_height)),
        text=f"Mnożnik graw. piasku: {current_settings['sand_gravity_multiplier']:.2f}", manager=manager
    )
    y_offset += label_height + spacing
    sand_gravity_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((menu_x_start + 10, y_offset), (menu_width - 20, slider_height)),
        start_value=current_settings['sand_gravity_multiplier'], value_range=(0.01, 1.0), manager=manager
    )
    y_offset += slider_height + spacing * 2
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((menu_x_start + 10, y_offset), (menu_width - 20, label_height)),
        text='Parametry Bomby:', manager=manager, object_id='#section_header'
    )
    y_offset += label_height + spacing
    bomb_scale_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((menu_x_start + 10, y_offset), (menu_width - 20, label_height)),
        text=f"Skala bomby: {current_settings.get('bomb_visual_scale', DEFAULT_BOMB_VISUAL_SCALE):.2f}", manager=manager
    )
    y_offset += label_height + spacing
    bomb_scale_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((menu_x_start + 10, y_offset), (menu_width - 20, slider_height)),
        start_value=current_settings.get('bomb_visual_scale', DEFAULT_BOMB_VISUAL_SCALE),
        value_range=(0.1, 2.0), manager=manager
    )
    y_offset += slider_height + spacing * 2
    save_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((menu_x_start + 10, y_offset), (menu_width - 20, button_height)),
        text='Zapisz Ustawienia', manager=manager
    )
    y_offset += button_height + spacing
    reset_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((menu_x_start + 10, y_offset), (menu_width - 20, button_height)),
        text='Resetuj Symulację', manager=manager
    )
    gui_texture_id = glGenTextures(1)
    glClearColor(0.0, 0.0, 0.1, 1.0)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_PROGRAM_POINT_SIZE)
    angle_y = 0
    angle_x = 0
    camera_zoom = -6
    particles = [Particle(initial_explosion_scale=global_explosion_scale, params=current_settings) for _ in range(NUM_PARTICLES)]
    sand_particles = [SandParticle(initial_explosion_scale=global_explosion_scale, params=current_settings) for _ in range(NUM_SAND_PARTICLES)]
    bomb = Bomb()
    shockwave = Shockwave()
    clock = pygame.time.Clock()
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        time_delta = dt
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    if event.pos[0] < scene_width: camera_zoom += 0.5
                if event.button == 5:
                    if event.pos[0] < scene_width: camera_zoom -= 0.5
            manager.process_events(event)
            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == scale_slider:
                    global_explosion_scale = event.value
                    current_settings['explosion_scale'] = global_explosion_scale
                    scale_label.set_text(f'Skala eksplozji: {global_explosion_scale:.2f}')
                    for p in particles: p.explosion_scale = global_explosion_scale
                    for sp in sand_particles: sp.explosion_scale = global_explosion_scale
                elif event.ui_element == cloud_spread_min_slider:
                    current_settings['cloud_spread_speed_min'] = event.value
                    cloud_spread_label.set_text(f"Rozrzut: {current_settings['cloud_spread_speed_min']:.2f}-{current_settings['cloud_spread_speed_max']:.2f}")
                elif event.ui_element == cloud_spread_max_slider:
                    current_settings['cloud_spread_speed_max'] = event.value
                    cloud_spread_label.set_text(f"Rozrzut: {current_settings['cloud_spread_speed_min']:.2f}-{current_settings['cloud_spread_speed_max']:.2f}")
                elif event.ui_element == cloud_air_resistance_slider:
                    current_settings['cloud_air_resistance'] = event.value
                    cloud_air_resistance_label.set_text(f"Opór pow. chmury: {current_settings['cloud_air_resistance']:.4f}")
                elif event.ui_element == sand_speed_min_slider:
                    current_settings['sand_speed_min'] = event.value
                    sand_speed_label.set_text(f"Prędkość piasku: {current_settings['sand_speed_min']:.2f}-{current_settings['sand_speed_max']:.2f}")
                elif event.ui_element == sand_speed_max_slider:
                    current_settings['sand_speed_max'] = event.value
                    sand_speed_label.set_text(f"Prędkość piasku: {current_settings['sand_speed_min']:.2f}-{current_settings['sand_speed_max']:.2f}")
                elif event.ui_element == sand_gravity_slider:
                    current_settings['sand_gravity_multiplier'] = event.value
                    sand_gravity_label.set_text(f"Mnożnik graw. piasku: {current_settings['sand_gravity_multiplier']:.2f}")
                elif event.ui_element == bomb_scale_slider:
                    current_settings['bomb_visual_scale'] = event.value
                    bomb_scale_label.set_text(f"Skala bomby: {current_settings['bomb_visual_scale']:.2f}")
                for p in particles: p.params = current_settings
                for sp in sand_particles: sp.params = current_settings
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == reset_button:
                    reset_simulation(bomb, particles, sand_particles, shockwave, scale_slider, scale_label)
                elif event.ui_element == save_button:
                    save_settings(scale_slider)
        keys = pygame.key.get_pressed()
        mouse_x, _ = pygame.mouse.get_pos()
        can_control_camera = mouse_x < scene_width and not manager.get_focus_set()
        if can_control_camera:
            if keys[K_LEFT]: angle_y -= 1
            if keys[K_RIGHT]: angle_y += 1
            if keys[K_UP]: angle_x -= 1
            if keys[K_DOWN]: angle_x += 1
        angle_x = max(-89.0, min(89.0, angle_x))
        camera_zoom = max(-20.0, min(-2.0, camera_zoom))
        if not bomb.exploded:
            sand_shot_this_explosion = False
            particles_activated_this_explosion = False
        bomb.update(dt)
        if bomb.exploded:
            if not shockwave.active:
                shockwave.start(scale=global_explosion_scale)
            if not particles_activated_this_explosion:
                for p in particles:
                    p.explosion_scale = global_explosion_scale
                    p.params = current_settings
                    p.activate()
                particles_activated_this_explosion = True
            if not sand_shot_this_explosion:
                for sp in sand_particles:
                    sp.explosion_scale = global_explosion_scale
                    sp.params = current_settings
                    sp.activate()
                sand_shot_this_explosion = True
            shockwave.update(dt)
            for p in particles: p.update(dt)
            for sp in sand_particles: sp.update(dt)
        else:
            for p in particles: p.update(dt)
            for sp in sand_particles: sp.update(dt)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, scene_width, HEIGHT)
        glMatrixMode(GL_PROJECTION); glLoadIdentity()
        gluPerspective(45, (scene_width / float(HEIGHT)), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW); glLoadIdentity()
        glTranslatef(0.0, -0.6, camera_zoom)
        glRotatef(angle_x, 1, 0, 0); glRotatef(angle_y, 0, 1, 0)
        draw_background_sides()
        crater_radius_val = 1.2 * global_explosion_scale
        if bomb.exploded:
            draw_ground(crater_present=True, crater_radius=crater_radius_val)
            draw_crater(radius=crater_radius_val)
        else:
            draw_ground(crater_present=False)
        bomb.draw(scale=current_settings.get('bomb_visual_scale', DEFAULT_BOMB_VISUAL_SCALE))
        if bomb.exploded:
            shockwave.draw()
            for p in particles:
                if p.active: p.draw()
            for sp in sand_particles:
                if sp.active: sp.draw()
        manager.update(time_delta)
        gui_surface.fill((0, 0, 0, 0))
        menu_rect_on_gui_surface = pygame.Rect(menu_x_start, 0, menu_width, HEIGHT)
        pygame.draw.rect(gui_surface, (50, 50, 70, 255), menu_rect_on_gui_surface)
        manager.draw_ui(gui_surface)
        texture_surface_data = pygame.image.tobytes(gui_surface, "RGBA", flipped=True)
        gui_width, gui_height = gui_surface.get_size()
        glViewport(0, 0, gui_width, gui_height)
        glMatrixMode(GL_PROJECTION); glPushMatrix(); glLoadIdentity()
        gluOrtho2D(0, gui_width, gui_height, 0)
        glMatrixMode(GL_MODELVIEW); glPushMatrix(); glLoadIdentity()
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, gui_texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, gui_width, gui_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_surface_data)
        glColor4f(1.0, 1.0, 1.0, 1.0)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 1); glVertex2f(0, 0)
        glTexCoord2f(1, 1); glVertex2f(gui_width, 0)
        glTexCoord2f(1, 0); glVertex2f(gui_width, gui_height)
        glTexCoord2f(0, 0); glVertex2f(0, gui_height)
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glMatrixMode(GL_PROJECTION); glPopMatrix()
        glMatrixMode(GL_MODELVIEW); glPopMatrix()
        pygame.display.flip()
    glDeleteTextures([gui_texture_id])
    pygame.quit()

if __name__ == '__main__':
    main()