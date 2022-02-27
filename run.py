import pygame
import math


pygame.init()

WIDTH, HEIGH = 600, 600

WIN = pygame.display.set_mode((WIDTH, HEIGH))
pygame.display.set_caption('Satelite race')

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

class Planet:

    ASTRONOMICAL_UNIT = 149.6e6 * 1000
    GRAVITATIONAL_UNIT = 6.67428e-11
    SCALE = 250 / ASTRONOMICAL_UNIT # 1 ASTRONOMICAL_UNIT = 100 pixels
    TIMESTEP = 3600 * 24 # 1 DAY IN SECONDS

    def __init__(self, x, y, radius, color, mass):

        self.x = x 
        self.y = y 
        self.radius = radius 
        self.color = color
        self.mass = mass

        self.is_sun = False
        self.distance_to_sun = 0
        self.orbit = []

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGH/2

        pygame.draw.circle(win, self.color, (x, y), self.radius)

def main():

    run = True
    clock = pygame.time.Clock()
    
    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10 ** 30)
    sun.is_sun = True

    planets = [sun]

    while run:
        clock.tick(60)
        # WIN.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.draw(WIN)

        pygame.display.update()
    
    pygame.quit()


if __name__ == "__main__":
    
    main()