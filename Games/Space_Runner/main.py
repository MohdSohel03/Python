import pygame
import random
import os

pygame.init()

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Runner")

# Clock
clock = pygame.time.Clock()

# Colors
WHITE, BLACK, GREEN = (255, 255, 255), (0, 0, 0), (0, 255, 0)

# Assets
BACKGROUND_IMG = pygame.transform.scale(pygame.image.load("assets/background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
PLAYER_IMG = pygame.transform.smoothscale(pygame.image.load("assets/player.png"), (50, 60))
ASTEROID_IMG = pygame.transform.smoothscale(pygame.image.load("assets/asteroid.png"), (50, 50))
COLLECTIBLE_IMG = pygame.transform.smoothscale(pygame.image.load("assets/star.png"), (30, 30))
SHIELD_IMG = pygame.transform.smoothscale(pygame.image.load("assets/shield.png"), (70, 70))

# Sounds
pygame.mixer.music.load("assets/music.mp3")
pygame.mixer.music.play(-1)
JUMP_SOUND = pygame.mixer.Sound("assets/jump.mp3")
COLLECT_SOUND = pygame.mixer.Sound("assets/collect.wav")
HIT_SOUND = pygame.mixer.Sound("assets/hit.wav")
SHIELD_SOUND = pygame.mixer.Sound("assets/shield.wav")

# Fonts
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 48)

# Game state
GROUND_Y = SCREEN_HEIGHT - 40
player_rect = pygame.Rect(100, GROUND_Y - 60, 50, 60)
vertical_velocity = 0
gravity = 0.8
is_jumping = False
shield_active = False
shield_timer = 0
shield = None
score = 0
lives = 3
high_score = 0
paused = False
mute = False
volume = 1.0

# Load high score from file
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as f:
        try:
            high_score = int(f.read())
        except ValueError:
            high_score = 0

# Entities
obstacles = []
collectibles = []

def draw_volume_bar():
    pygame.draw.rect(WIN, WHITE, (SCREEN_WIDTH - 160, 10, 150, 20), 2)
    pygame.draw.rect(WIN, GREEN, (SCREEN_WIDTH - 158, 12, int(volume * 146), 16))

def draw_powerup_bar():
    if shield_active:
        elapsed = (pygame.time.get_ticks() - shield_timer) / 5000
        pygame.draw.rect(WIN, WHITE, (10, 100, 150, 10), 2)
        pygame.draw.rect(WIN, GREEN, (12, 102, int((1 - elapsed) * 146), 6))

def draw_window():
    WIN.blit(BACKGROUND_IMG, (0, 0))
    WIN.blit(PLAYER_IMG, player_rect.topleft)

    for o in obstacles:
        WIN.blit(o["image"], o["rect"].topleft)
    for c in collectibles:
        WIN.blit(c["image"], c["rect"].topleft)

    if shield_active:
        WIN.blit(SHIELD_IMG, (player_rect.x - 10, player_rect.y - 10))

    pygame.draw.line(WIN, WHITE, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 2)

    WIN.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
    WIN.blit(font.render(f"Lives: {lives}", True, WHITE), (10, 40))
    WIN.blit(font.render(f"High Score: {high_score}", True, WHITE), (10, 70))

    draw_volume_bar()
    draw_powerup_bar()

    pygame.display.update()

def start_menu():
    while True:
        WIN.fill(BLACK)
        title = big_font.render("Space Runner", True, WHITE)
        start_btn = font.render("Press [S] to Start", True, WHITE)
        mute_btn = font.render("Press [M] to Mute/Unmute", True, WHITE)
        quit_btn = font.render("Press [Q] to Quit", True, WHITE)
        WIN.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))
        WIN.blit(start_btn, (SCREEN_WIDTH // 2 - start_btn.get_width() // 2, 150))
        WIN.blit(mute_btn, (SCREEN_WIDTH // 2 - mute_btn.get_width() // 2, 200))
        WIN.blit(quit_btn, (SCREEN_WIDTH // 2 - quit_btn.get_width() // 2, 250))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            return
        if keys[pygame.K_m]:
            global mute
            mute = not mute
            pygame.mixer.music.set_volume(0 if mute else volume)
            pygame.time.wait(200)
        if keys[pygame.K_q]:
            pygame.quit()
            exit()

def game_over_screen():
    global high_score
    if score > high_score:
        high_score = score
        with open("highscore.txt", "w") as f:
            f.write(str(high_score))

    while True:
        WIN.fill(BLACK)
        msg = big_font.render("Game Over", True, WHITE)
        restart = font.render("Press [R] to Restart", True, WHITE)
        WIN.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 120))
        WIN.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, 200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        if pygame.key.get_pressed()[pygame.K_r]:
            return

def main():
    global is_jumping, vertical_velocity, obstacles, collectibles, score, shield, shield_active, shield_timer, lives, paused, volume

    start_menu()
    run = True
    obstacle_timer = 0
    collectible_timer = 0
    shield_spawn_timer = 0

    player_rect.y = GROUND_Y - player_rect.height
    vertical_velocity = 0
    is_jumping = False
    score = 0
    lives = 3
    obstacles.clear()
    collectibles.clear()
    shield = None
    shield_active = False

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            paused = not paused
            pygame.time.wait(300)
        if keys[pygame.K_UP]:
            volume = min(1.0, volume + 0.01)
            pygame.mixer.music.set_volume(volume if not mute else 0)
        if keys[pygame.K_DOWN]:
            volume = max(0.0, volume - 0.01)
            pygame.mixer.music.set_volume(volume if not mute else 0)

        if paused:
            WIN.blit(font.render("Paused. Press P to resume.", True, WHITE), (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
            pygame.display.update()
            continue

        if not is_jumping and keys[pygame.K_SPACE]:
            is_jumping = True
            vertical_velocity = -14
            if not mute:
                JUMP_SOUND.play()

        if is_jumping:
            player_rect.y += vertical_velocity
            vertical_velocity += gravity
            if player_rect.y >= GROUND_Y - player_rect.height:
                player_rect.y = GROUND_Y - player_rect.height
                is_jumping = False
                vertical_velocity = 0

        obstacle_timer += 1
        if obstacle_timer > 90:
            obstacle = {"rect": pygame.Rect(SCREEN_WIDTH, GROUND_Y - 50, 50, 50), "image": ASTEROID_IMG}
            obstacles.append(obstacle)
            obstacle_timer = 0

        collectible_timer += 1
        if collectible_timer > 150:
            collectible = {"rect": pygame.Rect(SCREEN_WIDTH, GROUND_Y - 30, 30, 30), "image": COLLECTIBLE_IMG}
            collectibles.append(collectible)
            collectible_timer = 0

        shield_spawn_timer += 1
        if not shield and shield_spawn_timer > 400:
            shield = {"rect": pygame.Rect(SCREEN_WIDTH, GROUND_Y - 70, 70, 70), "image": SHIELD_IMG}
            shield_spawn_timer = 0

        for o in obstacles:
            o["rect"].x -= 5
        obstacles = [o for o in obstacles if o["rect"].right > 0]

        for c in collectibles:
            c["rect"].x -= 5
        collectibles = [c for c in collectibles if c["rect"].right > 0]

        if shield:
            shield["rect"].x -= 5
            if shield["rect"].right < 0:
                shield = None

        for o in obstacles[:]:
            if player_rect.colliderect(o["rect"]):
                if shield_active:
                    obstacles.remove(o)
                else:
                    lives -= 1
                    if not mute:
                        HIT_SOUND.play()
                    obstacles.remove(o)
                    if lives <= 0:
                        game_over_screen()
                        return main()

        for c in collectibles[:]:
            if player_rect.colliderect(c["rect"]):
                score += 10
                collectibles.remove(c)
                if not mute:
                    COLLECT_SOUND.play()

        if shield and player_rect.colliderect(shield["rect"]):
            shield_active = True
            shield_timer = pygame.time.get_ticks()
            if not mute:
                SHIELD_SOUND.play()
            shield = None

        if shield_active and pygame.time.get_ticks() - shield_timer > 5000:
            shield_active = False

        draw_window()

    pygame.quit()

if __name__ == "__main__":
    main()
