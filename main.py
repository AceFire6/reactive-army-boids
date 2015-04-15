from boid import Boid
from enemy import Enemy
import config
import pygame


def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_c:
                config.DRAW_COLLISION = not config.DRAW_COLLISION
            elif event.key == pygame.K_v:
                config.DRAW_VISION = not config.DRAW_VISION
            elif event.key == pygame.K_q:
                config.COLLISION_RANGE -= (5 if config.COLLISION_RANGE >= 6
                                           else 0)
            elif event.key == pygame.K_w:
                config.COLLISION_RANGE += 5
            elif event.key == pygame.K_a:
                config.VISION_RANGE -= 5 if config.VISION_RANGE >= 6 else 0
            elif event.key == pygame.K_s:
                config.VISION_RANGE += 5
            elif event.key == pygame.K_ESCAPE:
                return False
            elif event.key == pygame.K_F1:
                config.FORMATION = not config.FORMATION
                print "Formation:", config.FORMATION
            elif event.key == pygame.K_F2:
                config.BOUNDARY = not config.BOUNDARY
                print "Boundary:", config.BOUNDARY
            elif event.key == pygame.K_F3:
                config.AVOID = not config.AVOID
                print "Avoid:", config.AVOID
            elif event.key == pygame.K_F4:
                config.VELOCITY = not config.VELOCITY
                print "Velocity:", config.VELOCITY
            elif event.key == pygame.K_F5:
                config.CENTER_MASS = not config.CENTER_MASS
                print "Center Mass:", config.CENTER_MASS
    return True


def loop(entities, obstacles=None):
    for entity in entities:
        if obstacles:
            entity.apply_velocity(entities, obstacles)
        else:
            entity.apply_velocity(entities)


def render(screen, entities):
    screen.fill((0, 0, 0))
    for entity in entities:
        pygame.draw.polygon(screen, entity.colour, entity.vertices)
        if config.DRAW_COLLISION:
            pygame.draw.circle(screen, entity.colour, entity.get_center(),
                               config.COLLISION_RANGE, 1)
        if config.DRAW_VISION:
            pygame.draw.circle(screen, entity.colour, entity.get_center(),
                               config.VISION_RANGE, 1)
    pygame.draw.circle(screen, (255, 255, 255), config.F_CENTER,
                       config.F_RADIUS, 1)
    pygame.display.flip()

def main():
    pygame.init()
    pygame.display.set_caption("Boids - Prototype")
    screen = pygame.display.set_mode(
        (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    running = True

    boids = [Boid() for i in range(config.NUM_BOIDS)]
    enemies = [Enemy((2, 0))]
    clock = pygame.time.Clock()
    while running:
        clock.tick(60)
        pygame.time.wait(1)
        running = events()
        loop(boids, obstacles=enemies)
        loop(enemies)
        render(screen, boids + enemies)

if __name__ == "__main__":
    main()
