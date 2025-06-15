# 🚀 Space Runner - Pygame

An animated, music-backed space runner game with shields, power-ups, parallax backgrounds, and saved high scores.

## 🎮 Features
- Player sprite with shield power-ups
- Collectibles and asteroids
- Parallax background animation
- Start/Pause/Game Over menus
- Background music and sound effects
- Volume control
- High score saving

## 📁 Folder Structure

- `assets/images/`: All image sprites
- `assets/sounds/`: Background music and SFX
- `highscore.txt`: Stores highest score between runs
- `main.py`: Game code
- `README.md`: Info & instructions

📁 assets/ Folder
Contains all game visuals and sounds.

player.png → Your player character sprite
asteroid.png → Obstacle image
star.png → Collectible image
shield.png → Visual for active shield power-up
parallax_bg.png → A wide parallax background image
background_music.mp3 → Looping background soundtrack
collect.wav → Played on collectible pickup
hit.wav → Played on collision
powerup.wav → Played on power-up collection

## ▶️ Running the Game

Make sure Python and Pygame are installed:
```bash
pip install pygame
python main.py

