from Tkinter import *
import tkFileDialog
from enemy import Enemy
from formation import Formation
import config
import pygame
from vec2d import Vec2d

units = []  # Units in the formation
enemies = []  # Enemies added by the user
formation = None  # The formation being used
enemy_start = None  # The start point of the current enemy path


def events():
    """Event section of game loop. Handle user input. Return boolean."""
    global units, enemies, formation, enemy_start
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Program window quit button press
            return False
        elif event.type == pygame.KEYUP:  # Key pressed event
            if event.key == pygame.K_r:
                units = []
                enemies = []
                formation = None
                enemy_start = None
            elif event.key == pygame.K_ESCAPE:
                return False
            elif event.key == pygame.K_o and (pygame.key.get_mods() &
                                              pygame.KMOD_CTRL):  # Open file
                options = {
                    'filetypes': [('Formations', '.fm')],
                    'title': 'Open formation'}
                formation = Formation(tkFileDialog.askopenfile('r', **options))
                units = formation.gen_and_get_boids()
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Mouse event
            states = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            if states == (1, 0, 0):  # Left click - set enemy path
                if not enemy_start:
                    enemy_start = mouse_pos
                else:
                    enemies.append(Enemy(Vec2d(enemy_start), Vec2d(mouse_pos)))
                    enemy_start = None
            elif states == (0, 0, 1):  # Right click - set waypoint
                if formation:
                    formation.set_waypoint(mouse_pos)
    return True


def update(obstacles=None):
    """Update the formation and units."""
    global units, formation
    if formation:
        formation.update()
    for unit in units:
        if obstacles:
            unit.update(units, obstacles)
        else:
            unit.update(units)
    for enemy in enemies:
        enemy.update()


def render(screen):
    """Render section of game loop. Handle drawing."""
    global units, formation
    screen.fill((0, 0, 0))
    if formation:
        pygame.draw.circle(screen, (0, 100, 200), formation.center, 5, 0)
    for unit in units:
        pygame.draw.polygon(screen, unit.colour, unit.vertices)
    for enemy in enemies:
        pygame.draw.polygon(screen, config.RED, enemy.vertices)
    pygame.display.flip()


def main():
    """Main game loop. Loop until events returns false."""
    pygame.init()
    pygame.display.set_caption("Reactive Formations")
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
        update(enemies) if enemies else update()
        render(screen)

if __name__ == "__main__":
    main()
