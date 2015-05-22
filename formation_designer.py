from Tkinter import *
import tkFileDialog
import pygame
import config
import math


boundaries = True


def distance_to(point1, point2):
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)


def close_to(point, placed_units):
    return [unit for unit in placed_units
            if distance_to(point, unit) < config.COLLISION_RANGE]


def get_closest(point, close_units):
    if close_units:
        closest = close_units[0]
        dist = distance_to(point, closest)

        for close_unit in close_units:
            temp_dist = distance_to(point, close_unit)
            if temp_dist < dist:
                closest = close_unit
                dist = temp_dist
        return closest
    return None


def get_closest_and_dist(point, close_units):
    closest = get_closest(point, close_units)
    if closest:
        return closest, distance_to(point, closest)
    else:
        return closest, -1


def events(placed_units):
    global boundaries
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            elif event.key == pygame.K_SPACE:
                boundaries = not boundaries
            elif event.key == pygame.K_s and (pygame.key.get_mods() &
                                              pygame.KMOD_CTRL):
                options = {
                    'filetypes': [('Formations', '.fm')],
                    'initialfile': 'formation1.fm',
                    'title': 'Save the formation'}
                save_file = tkFileDialog.asksaveasfile('w', **options)
                if save_file:
                    for placed_unit in placed_units:
                        save_file.write(str(placed_unit) + '\n')
                    save_file.close()
            elif event.key == pygame.K_o and (pygame.key.get_mods() &
                                              pygame.KMOD_CTRL):
                options = {
                    'filetypes': [('Formations', '.fm')],
                    'title': 'Open formation'}
                open_file = tkFileDialog.askopenfile('r', **options)
                if open_file:
                    for line in open_file.readlines():
                        new_point = eval(line)
                        if not close_to(new_point, placed_units):
                            placed_units.append(new_point)
                    open_file.close()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            states = pygame.mouse.get_pressed()
            config.debug_print("STATES:", states)
            mouse_pos = pygame.mouse.get_pos()
            close_units = close_to(mouse_pos, placed_units)
            if states == (1, 0, 0): # Left click - Add
                if not close_units:
                    placed_units.append(mouse_pos)
            elif states == (0, 0, 1): # Right click - Delete
                if close_units:
                    placed_units.remove(get_closest(mouse_pos, close_units))

    return True


def render(screen, placed_units):
    global boundaries
    screen.fill((0, 0, 0))
    colour = config.WHITE
    closest_to_mouse, dist = get_closest_and_dist(pygame.mouse.get_pos(),
                                                  placed_units)
    for unit in placed_units:
        if unit == closest_to_mouse and dist <= config.COLLISION_RANGE:
            colour = config.RED
        if boundaries:
            pygame.draw.circle(screen, colour, unit,
                               config.COLLISION_RANGE, 1)
        pygame.draw.circle(screen, colour, unit,
                           2, 0)
        colour = config.WHITE
    pygame.display.flip()


def main():
    pygame.init()
    pygame.display.set_caption('Formation Designer')
    screen = pygame.display.set_mode(
        (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    running = True

    win = Tk()
    win.withdraw()

    placed_units = []

    clock = pygame.time.Clock()
    while running:
        clock.tick(60)
        pygame.time.wait(1)
        running = events(placed_units)
        render(screen, placed_units)


if __name__ == "__main__":
    main()
