from Tkinter import *
import tkFileDialog
from enemy import Enemy
from formation import Formation
import config
import pygame
from vec2d import Vec2d

boids = []
enemies = []
formation = None
enemy_start = None


def events():
    global boids, enemies, formation, enemy_start
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                boids = []
                enemies = []
                formation = None
                enemy_start = None
            elif event.key == pygame.K_ESCAPE:
                return False
            elif event.key == pygame.K_o and (pygame.key.get_mods() &
                                              pygame.KMOD_CTRL):
                options = {
                    'filetypes': [('Formations', '.fm')],
                    'title': 'Open formation'}
                formation = Formation(tkFileDialog.askopenfile('r', **options))
                boids = formation.gen_and_get_boids()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            states = pygame.mouse.get_pressed()
            config.debug_print("STATES:", states)
            mouse_pos = pygame.mouse.get_pos()
            if states == (1, 0, 0): # Left click
                if not enemy_start:
                    enemy_start = mouse_pos
                else:
                    enemies.append(Enemy(Vec2d(enemy_start), Vec2d(mouse_pos)))
                    enemy_start = None
            elif states == (0, 0, 1): # Right click
                if formation:
                    formation.set_waypoint(mouse_pos)
    return True


def loop(obstacles=None):
    global boids, formation
    if formation:
        formation.update()
    for boid in boids:
        if obstacles:
            boid.update(boids, obstacles)
        else:
            boid.update(boids)
    for enemy in enemies:
        enemy.update()


def render(screen):
    global boids, formation
    screen.fill((0, 0, 0))
    if formation:
        pygame.draw.circle(screen, (0, 100, 200), formation.center, 5, 0)
    for boid in boids:
        pygame.draw.polygon(screen, boid.colour, boid.vertices)
    for enemy in enemies:
        pygame.draw.polygon(screen, config.RED, enemy.vertices)
    pygame.display.flip()


def main():
    pygame.init()
    pygame.display.set_caption("Boids - Prototype")
    screen = pygame.display.set_mode(
        (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    running = True

    win = Tk()
    win.withdraw()

    clock = pygame.time.Clock()
    while running:
        clock.tick(60)
        pygame.time.wait(1)
        running = events()
        loop(enemies) if enemies else loop()
        render(screen)

if __name__ == "__main__":
    main()
