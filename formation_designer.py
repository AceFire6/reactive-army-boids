import pygame
import config


def close_to(point, placed_units):
    return [unit for unit in placed_units
            if ((point[0] - unit[0])**2 + (point[1] - unit[1])**2) < 100]

def events(placed_units):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            states = pygame.mouse.get_pressed()
            config.debug_print("STATES:", states)
            mouse_pos = pygame.mouse.get_pos()
            if states == (1, 0, 0): # Left click - Add
                placed_units.append(mouse_pos)
            elif states == (0, 0, 1): # Right click - Delete
                pass

    return True


def render(screen, placed_units):
    screen.fill((0, 0, 0))
    for unit in placed_units:
        pygame.draw.circle(screen, config.WHITE, unit,
                           config.COLLISION_RANGE, 1)
    pygame.display.flip()


def main():
    pygame.init()
    pygame.display.set_caption('Formation Designer')
    screen = pygame.display.set_mode(
        (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    running = True

    placed_units = []

    clock = pygame.time.Clock()
    while running:
        clock.tick(60)
        pygame.time.wait(1)
        running = events(placed_units)
        render(screen, placed_units)


if __name__ == "__main__":
    main()
