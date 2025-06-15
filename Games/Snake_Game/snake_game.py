import pygame
import time
import random
import os
import json
from pygame.locals import *

# Initialize Pygame and the mixer for sounds
pygame.init()
pygame.mixer.init()

# Screen setup
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced Snake Game")

# Set the game icon (Windows-style)
icon_path = os.path.join("assets", "game_icon.png")
game_icon = pygame.image.load(icon_path)
pygame.display.set_icon(game_icon)

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
GOLD = (255, 215, 0)
BG_COLOR = (10, 10, 30)

# Settings
BLOCK_SIZE = 10
DEFAULT_SPEED = 15

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Files
BASE_DIR = os.path.dirname(__file__)
EAT_SOUND = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets", "eat_sound.mp3"))
DIE_SOUND = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets", "die_sound.mp3"))
BONUS_EAT_SOUND = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets", "eat_sound.mp3"))
SNAKE_HIT_SOUND = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets", "die_sound.mp3"))
SAVE_FILE = os.path.join(BASE_DIR, "save_game.txt")
HIGH_SCORE_FILE = os.path.join(BASE_DIR, "high_score.txt")

# High Score Helpers
def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    if score > load_high_score():
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(score))

# Save and Load Game State
def save_game(state):
    with open(SAVE_FILE, "w") as f:
        json.dump(state, f)

def load_game():
    try:
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    except:
        return None

# Display score
def your_score(score):
    value = score_font.render(f"Score: {score}", True, WHITE)
    screen.blit(value, [WIDTH - 200, 10])

# Draw snake
def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.circle(screen, GREEN, (int(x[0] + BLOCK_SIZE/2), int(x[1] + BLOCK_SIZE/2)), BLOCK_SIZE // 2)

# Draw food
def draw_food(pos, kind):
    color = GOLD if kind == "gold" else YELLOW
    pygame.draw.rect(screen, color, [pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE])

# Message display
def message(msg, color, y_offset=0):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [WIDTH / 6, HEIGHT / 3 + y_offset])

# Select difficulty
def select_difficulty():
    screen.fill(BG_COLOR)
    message("Select Difficulty:", WHITE, -40)
    message("1 - Easy    2 - Medium    3 - Hard", YELLOW, 10)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: return 10
                if event.key == pygame.K_2: return 15
                if event.key == pygame.K_3: return 20

# Start menu
def show_start_menu():
    screen.fill(BG_COLOR)
    message("Welcome to Snake Game!", GREEN, -30)
    message("Press SPACE to Play or Q to Quit", WHITE, 20)
    if load_game():
        message("Press L to Load Last Game", GOLD, 50)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: return "new"
                if event.key == pygame.K_l: return "load"
                if event.key == pygame.K_q: pygame.quit(); quit()

# Main game loop
def gameLoop():
    mode = show_start_menu()
    speed = select_difficulty() if mode == "new" else DEFAULT_SPEED

    if mode == "load":
        state = load_game()
        if not state: return gameLoop()
        x1 = state["x1"]
        y1 = state["y1"]
        x1_change = state["x1_change"]
        y1_change = state["y1_change"]
        snake_list = state["snake_list"]
        length = state["length"]
        food = state["food"]
        food_type = state["food_type"]
        score = state["score"]
    else:
        x1, y1 = WIDTH / 2, HEIGHT / 2
        x1_change, y1_change = 0, 0
        snake_list = []
        length = 1
        food = [random.randrange(0, WIDTH - BLOCK_SIZE, 10), random.randrange(0, HEIGHT - BLOCK_SIZE, 10)]
        food_type = "regular"
        score = 0

    game_close = False
    clock = pygame.time.Clock()
    paused = False

    # Game loop
    while not game_close:
        while paused:
            screen.fill(BLACK)
            message("Paused - Press P to Resume", WHITE, 0)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    paused = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game({
                    "x1": x1, "y1": y1,
                    "x1_change": x1_change, "y1_change": y1_change,
                    "snake_list": snake_list,
                    "length": length,
                    "food": food,
                    "food_type": food_type,
                    "score": score
                })
                game_close = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change, y1_change = -BLOCK_SIZE, 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change, y1_change = BLOCK_SIZE, 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change, x1_change = -BLOCK_SIZE, 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change, x1_change = BLOCK_SIZE, 0
                elif event.key == pygame.K_p:
                    paused = True

        x1 += x1_change
        y1 += y1_change

        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            SNAKE_HIT_SOUND.play()
            break

        screen.fill(BG_COLOR)
        draw_food(food, food_type)

        head = [x1, y1]
        snake_list.append(head)
        if len(snake_list) > length:
            del snake_list[0]

        for seg in snake_list[:-1]:
            if seg == head:
                SNAKE_HIT_SOUND.play()
                game_close = True

        draw_snake(snake_list)
        your_score(score)
        pygame.display.update()

        # Eat food
        if x1 == food[0] and y1 == food[1]:
            EAT_SOUND.play()
            screen.fill(WHITE)
            pygame.display.update()
            time.sleep(0.05)
            length += 3 if food_type == "gold" else 1
            score += 3 if food_type == "gold" else 1
            food = [random.randrange(0, WIDTH - BLOCK_SIZE, 10), random.randrange(0, HEIGHT - BLOCK_SIZE, 10)]
            food_type = "gold" if random.random() < 0.1 else "regular"

        clock.tick(speed)

    save_high_score(score)
    time.sleep(2)
    pygame.quit()
    quit()

gameLoop()
