import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Window setup
WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 Space Runner")

clock = pygame.time.Clock()
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Font
font = pygame.font.SysFont(None, 48)
big_font = pygame.font.SysFont(None, 72)

# Ground
GROUND_Y = 300

# Constants
GRAVITY = 1
JUMP_STRENGTH = -18

# Game state
score = 0
game_over = False

# Initialize player and objects
def reset_game():
    global player_rect, player_velocity_y, is_jumping, asteroids, collectibles, score, game_over
    player_rect = pygame.Rect(100, GROUND_Y - 60, 50, 60)
    player_velocity_y = 0
    is_jumping = False
    asteroids = []
    collectibles = []
    score = 0
    game_over = False

# Obstacles & collectibles
asteroid_width, asteroid_height = 50, 50
asteroid_speed = 5
asteroid_spawn_timer = 0
asteroid_spawn_delay = 1500

collectible_width, collectible_height = 30, 30
collectible_speed = 5
collectible_spawn_timer = 0
collectible_spawn_delay = 2000

def spawn_asteroid():
    asteroid = pygame.Rect(WIDTH, GROUND_Y - asteroid_height, asteroid_width, asteroid_height)
    asteroids.append(asteroid)

def spawn_collectible():
    y_pos = random.randint(150, GROUND_Y - collectible_height - 10)
    collectible = pygame.Rect(WIDTH, y_pos, collectible_width, collectible_height)
    collectibles.append(collectible)

def draw_window():
    WIN.fill(BLACK)

    # Ground
    pygame.draw.line(WIN, WHITE, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)

    # Player
    pygame.draw.rect(WIN, (100, 200, 255), player_rect)

    # Asteroids
    for asteroid in asteroids:
        pygame.draw.rect(WIN, (200, 100, 100), asteroid)

    # Collectibles
    for collectible in collectibles:
        pygame.draw.rect(WIN, (255, 255, 0), collectible)

    # Score
    score_text = font.render(f"Score: {score}", True, WHITE)
    WIN.blit(score_text, (10, 10))

    # Game Over Message
    if game_over:
        over_text = big_font.render("GAME OVER", True, (255, 50, 50))
        restart_text = font.render("Press R to Restart", True, WHITE)
        WIN.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 60))
        WIN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))

    pygame.display.update()

def main():
    global is_jumping, player_velocity_y, asteroid_spawn_timer, collectible_spawn_timer, score, game_over

    reset_game()

    running = True
    while running:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if not game_over:
            # Handle jump
            if keys[pygame.K_SPACE] and not is_jumping:
                player_velocity_y = JUMP_STRENGTH
                is_jumping = True

            # Gravity
            player_velocity_y += GRAVITY
            player_rect.y += player_velocity_y

            # Ground collision
            if player_rect.bottom >= GROUND_Y:
                player_rect.bottom = GROUND_Y
                player_velocity_y = 0
                is_jumping = False

            # Asteroids
            asteroid_spawn_timer += dt
            if asteroid_spawn_timer > asteroid_spawn_delay:
                spawn_asteroid()
                asteroid_spawn_timer = 0

            for asteroid in asteroids[:]:
                asteroid.x -= asteroid_speed
                if asteroid.right < 0:
                    asteroids.remove(asteroid)
                elif asteroid.colliderect(player_rect):
                    game_over = True

            # Collectibles
            collectible_spawn_timer += dt
            if collectible_spawn_timer > collectible_spawn_delay:
                spawn_collectible()
                collectible_spawn_timer = 0

            for collectible in collectibles[:]:
                collectible.x -= collectible_speed
                if collectible.right < 0:
                    collectibles.remove(collectible)
                elif collectible.colliderect(player_rect):
                    collectibles.remove(collectible)
                    score += 1

        else:
            # Restart on R key
            if keys[pygame.K_r]:
                reset_game()

        draw_window()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
