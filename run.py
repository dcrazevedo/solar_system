import pygame
import math


pygame.init()

WIDTH, HEIGH = 900, 700

WIN = pygame.display.set_mode((WIDTH, HEIGH))
pygame.display.set_caption('Satelite race')

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GRAY = (80, 78, 81)

FONT = pygame.font.SysFont('comicsans', 16)

class Planet:

    ASTRONOMICAL_UNIT = 149.6e6 * 1000
    GRAVITATIONAL_UNIT = 6.67428e-11
    SCALE = 200 / ASTRONOMICAL_UNIT # 1 ASTRONOMICAL_UNIT = 100 pixels
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

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                point_x, point_y = point
                point_x = point_x * self.SCALE + WIDTH/2
                point_y = point_y * self.SCALE + HEIGH/2
                updated_points.append((point_x, point_y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)
        
        pygame.draw.circle(win, self.color, (int(x), int(y)), self.radius, 0)

        if not self.is_sun:
            distance_text = FONT.render(f'{round(self.distance_to_sun/1000, 1)}km', 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y + self.radius))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        
        distance_x = other_x - self.x
        distance_y = other_y - self.y

        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        if other.is_sun:
            self.distance_to_sun = distance

        force = self.GRAVITATIONAL_UNIT * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)

        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def main():

    run = True
    clock = pygame.time.Clock()
    
    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10 ** 30)
    sun.is_sun = True

    earth = Planet(-1 * Planet.ASTRONOMICAL_UNIT, 0, 16, BLUE, 5.9742 * 10 ** 24)
    earth.y_vel = 29.783 * 1000
    earth.is_sun = False

    mars = Planet(-1.524 * Planet.ASTRONOMICAL_UNIT, 0, 12, RED, 6.39 * 10 ** 23)
    mars.y_vel = 24.077 * 1000
    mars.is_sun = False
    
    mercury = Planet(0.387 * Planet.ASTRONOMICAL_UNIT, 0, 8, DARK_GRAY, 3.30 * 10 ** 23)
    mercury.y_vel = -47.4 * 1000
    mercury.is_sun = False
    
    venus = Planet(0.723 * Planet.ASTRONOMICAL_UNIT, 0, 14, WHITE, 4.8685 * 10 ** 23)
    venus.y_vel = -35.02 * 1000
    venus.is_sun = False

    planets = [sun, earth, mars, mercury, venus]

    while run:
        clock.tick(60)
        WIN.fill((0,0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()
    
    pygame.quit()


if __name__ == "__main__":
    
    main()