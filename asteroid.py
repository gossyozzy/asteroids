import pygame # type: ignore
from logger import log_event
from circleshape import CircleShape
from constants import LINE_WIDTH
from constants import ASTEROID_MIN_RADIUS
from constants import ASTEROID_MAX_RADIUS
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        asteroid_color = "yellow"
        if self.radius == ASTEROID_MIN_RADIUS:
            asteroid_color = "red"
        if self.radius == ASTEROID_MAX_RADIUS:
            asteroid_color = "green"
        pygame.draw.circle(screen, asteroid_color, self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += (self.velocity * dt)
    
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return 50
        
        log_event("asteroid_split")
        new_angle = random.uniform(20, 50)
        a1_vel = self.velocity.rotate(new_angle)
        a2_vel = self.velocity.rotate(-new_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        a1 = Asteroid(self.position.x, self.position.y, new_radius)
        a2 = Asteroid(self.position.x, self.position.y, new_radius)
        a1.velocity = a1_vel * 1.2
        a2.velocity = a2_vel * 1.2

        if self.radius >= ASTEROID_MAX_RADIUS:
            return 10
        if self.radius > ASTEROID_MIN_RADIUS:
            return 25
        
