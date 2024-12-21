import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Scavenger")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()
FPS = 60

SPACESHIP_IMAGE = pygame.image.load("resources/spaceship.png")
ASTEROID_IMAGE = pygame.image.load("resources/asteroid.png")
CRYSTAL_IMAGE = pygame.image.load("resources/energy_crystal.png")
BACKGROUND_IMAGE = pygame.image.load("resources/background.jpg")
CRASH_SOUND = pygame.mixer.Sound("resources/clash_sound.wav")
pygame.mixer.music.load("resources/background_music.wav")

SPACESHIP = pygame.transform.scale(SPACESHIP_IMAGE, (50, 50))
ASTEROID = pygame.transform.scale(ASTEROID_IMAGE, (60, 60))
CRYSTAL = pygame.transform.scale(CRYSTAL_IMAGE, (30, 30))
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))

spaceship_rect = SPACESHIP.get_rect(center=(WIDTH // 2, HEIGHT - 60))

asteroids = []
crystals = []

spaceship_speed = 5
asteroid_speed = 3
crystal_speed = 2

score = 0


def create_asteroid():
    x = random.randint(0, WIDTH - 60)
    y = random.randint(-100, -40)
    rect = ASTEROID.get_rect(topleft=(x, y))
    asteroids.append(rect)


def create_crystal():
    x = random.randint(0, WIDTH - 30)
    y = random.randint(-100, -40)
    rect = CRYSTAL.get_rect(topleft=(x, y))
    crystals.append(rect)


def draw_objects():
    screen.blit(BACKGROUND, (0, 0))
    screen.blit(SPACESHIP, spaceship_rect.topleft)
    for asteroid in asteroids:
        screen.blit(ASTEROID, asteroid.topleft)
    for crystal in crystals:
        screen.blit(CRYSTAL, crystal.topleft)
    draw_score()


def draw_score():
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))


def main():
    global score, spaceship_speed, asteroid_speed, crystal_speed

    pygame.mixer.music.play(-1)
    running = True

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and spaceship_rect.left > 0:
            spaceship_rect.x -= spaceship_speed
        if keys[pygame.K_RIGHT] and spaceship_rect.right < WIDTH:
            spaceship_rect.x += spaceship_speed

        for asteroid in asteroids[:]:
            asteroid.y += asteroid_speed
            if asteroid.top > HEIGHT:
                asteroids.remove(asteroid)
            if spaceship_rect.colliderect(asteroid):
                CRASH_SOUND.play()
                pygame.mixer.music.stop()
                game_over()
                return

        for crystal in crystals[:]:
            crystal.y += crystal_speed
            if crystal.top > HEIGHT:
                crystals.remove(crystal)
            if spaceship_rect.colliderect(crystal):
                crystals.remove(crystal)
                score += 10

        if score % 50 == 0 and score != 0:
            asteroid_speed += 0.2
            crystal_speed += 0.1
            spaceship_speed += 0.1

        if random.randint(1, 20) == 1:
            create_asteroid()
        if random.randint(1, 40) == 1:
            create_crystal()

        draw_objects()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


def game_over():
    font = pygame.font.Font(None, 74)
    text = font.render("GAME OVER", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)


if __name__ == "__main__":
    main()
