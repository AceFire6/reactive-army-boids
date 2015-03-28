from boid import Boid
import config
import pygame


def events():
    # event handling, gets all event from the eventqueue
    for event in pygame.event.get():
        # only do something if the event is of type QUIT
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_c:
                config.DRAW_COLLISION = not config.DRAW_COLLISION
            elif event.key == pygame.K_v:
                config.DRAW_VISION = not config.DRAW_VISION
            elif event.key == pygame.K_q:
                config.COLLISION_RANGE -= 5
            elif event.key == pygame.K_w:
                config.COLLISION_RANGE += 5
            elif event.key == pygame.K_a:
                config.VISION_RANGE -= 5
            elif event.key == pygame.K_s:
                config.VISION_RANGE += 5
    return True


def loop(boids):
    for boid in boids:
        boid.apply_velocity(boids)


def render(screen, boids):
    screen.fill((0, 0, 0))
    for boid in boids:
        pygame.draw.polygon(screen, boid.colour, boid.vertices)
        if config.DRAW_COLLISION:
            pygame.draw.circle(screen, boid.colour, boid.get_center(),
                               config.COLLISION_RANGE, 1)
        if config.DRAW_VISION:
            pygame.draw.circle(screen, boid.colour, boid.get_center(),
                               config.VISION_RANGE, 1)

    pygame.display.flip()


# define a main function
def main():
    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("Boids - Prototype")
    screen = pygame.display.set_mode(
        (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    running = True

    boids = [Boid() for i in range(config.NUM_BOIDS)]

    # main loop
    while running:
        pygame.time.wait(1)
        running = events()
        loop(boids)
        render(screen, boids)

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
