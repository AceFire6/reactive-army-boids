from Tkinter import *
import tkFileDialog
import pygame
import config
import math


center = None  # The center of the formation
# The vector direction - center is the direction the formation is facing
direction = None


def add_tuple(t1, t2):
    """Add each element of tuple t1 and t2 and return a tuple."""
    return tuple((t1[i] + t2[i]) for i in range(len(t1)))


def with_center(placed_units):
    """Return the list of the non-relative version of the placed_units."""
    global center
    return [add_tuple(placed_unit, center) for placed_unit in placed_units]


def distance_to(point1, point2):
    """Calculate the distance between point1 and point2 and return a float."""
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)


def close_to(point, placed_units):
    """Get all units close to point and return a list of these units."""
    return [unit for unit in placed_units
            if distance_to(point, unit) < config.COLLISION_RANGE + 10]


def get_closest(point, close_units):
    """Find the unit closest to point and return the closest tuple."""
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
    """Get the closest unit and the distance to it and return tuple."""
    closest = get_closest(point, close_units)
    if closest:
        return closest, distance_to(point, closest)
    else:
        return closest, -1


def events(placed_units):
    """Event section of the game loop. Handle user input. Return boolean."""
    global center, direction

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Program window quit button press
            return False
        elif event.type == pygame.KEYDOWN:  # Key pressed event
            if event.key == pygame.K_ESCAPE:
                return False
            elif event.key == pygame.K_s and (pygame.key.get_mods() &
                                              pygame.KMOD_CTRL):  # Save
                options = {
                    'filetypes': [('Formations', '.fm')],
                    'initialfile': 'formation1.fm',
                    'title': 'Save the formation'}
                save_file = tkFileDialog.asksaveasfile('w', **options)
                if save_file:
                    save_file.write(str(center) + '\n')
                    save_file.write(str(direction) + '\n')
                    for placed_unit in placed_units:
                        save_file.write(str(placed_unit) + '\n')
                    save_file.close()
            elif event.key == pygame.K_o and (pygame.key.get_mods() &
                                              pygame.KMOD_CTRL):  # Open
                options = {
                    'filetypes': [('Formations', '.fm')],
                    'title': 'Open formation'}
                open_file = tkFileDialog.askopenfile('r', **options)
                if open_file:
                    center = eval(open_file.readline())
                    direction = eval(open_file.readline())
                    for line in open_file.readlines()[0:]:
                        print line
                        placed_units.append(eval(line))
                    open_file.close()
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Mouse Event
            states = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            close_units = close_to(mouse_pos, with_center(placed_units))
            if states == (1, 0, 0):  # Left click - Add
                if not center:
                    center = mouse_pos
                    return True
                if not direction:
                    direction = (mouse_pos[0] - center[0],
                                 mouse_pos[1] - center[1])
                    return True
                if not close_units:
                    placed_units.append((mouse_pos[0] - center[0],
                                         mouse_pos[1] - center[1]))
            elif states == (0, 0, 1):  # Right click - Delete
                if close_units:
                    closest = get_closest(mouse_pos, close_units)
                    print (center[0] - closest[0], center[1] - closest[1])
                    placed_units.remove((closest[0] - center[0],
                                         closest[1] - center[1]))
    return True


def render(screen, placed_units):
    """Render section of game loop. Handle unit drawing."""
    global center
    screen.fill((0, 0, 0))
    colour = config.WHITE
    closest_to_mouse, dist = get_closest_and_dist(pygame.mouse.get_pos(),
                                                  with_center(placed_units))

    if center:
        pygame.draw.circle(screen, config.CYAN, center, 10, 0)
    if direction:
        pygame.draw.circle(screen, config.GREEN,
                           add_tuple(direction, center), 5, 0)

    for unit in with_center(placed_units):
        if unit == closest_to_mouse and dist <= config.COLLISION_RANGE + 10:
            colour = config.RED
        pygame.draw.circle(screen, colour, unit,
                           config.COLLISION_RANGE + 10, 1)
        pygame.draw.circle(screen, colour, unit,
                           2, 0)
        colour = config.WHITE
    pygame.display.flip()


def main():
    """Main game loop. Runs through every step of the game loop until the
    event section returns false.
    """
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
