import pygame # type: ignore
import sys
from constants import SCREEN_WIDTH
from constants import SCREEN_HEIGHT
from logger import log_state
from logger import log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.SysFont(None, 24)
    
    # print("Starting Asteroids with pygame version:", pygame.__version__)
    # print("Screen width:", SCREEN_WIDTH)
    # print("Screen height:", SCREEN_HEIGHT)

    game_clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable)
    Shot.containers = (updatable, drawable, shots)

    asteroid_field = AsteroidField()
    player = Player(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2)

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        text_surface = font.render("Score: " + str(player.score), True, "white")
        screen.blit(text_surface, (10, 10))

        updatable.update(dt)
        player.cooldown -= dt

        for obj in drawable:
            obj.draw(screen)
        
        for shot in shots:
            shot.draw(screen)
        
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
            
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    player.score += asteroid.split()
                    shot.kill()

        pygame.display.flip()
        dt = game_clock.tick(60) / 1000
        

if __name__ == "__main__":
    main()
