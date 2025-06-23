import pygame
import socket
import json
import os
import time

# Constants
WIDTH, HEIGHT = 1024, 728
WHITE = (255, 255, 255)
GREEN = (80, 166, 105)
BLACK = (0, 0, 0)
PINK = (223, 101, 146)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Theme Randomizer")
clock = pygame.time.Clock()

# Load custom fonts
FONT_PATH = "asset/fonts"
title_font = pygame.font.Font(os.path.join(FONT_PATH, "Roca Bold.ttf"), 60)
button_font = pygame.font.Font(os.path.join(FONT_PATH, "Roca Regular.ttf"), 32)
theme_font = pygame.font.Font(os.path.join(FONT_PATH, "Roca Regular.ttf"), 40)
desc_font = pygame.font.Font(os.path.join(FONT_PATH, "Roca Thin Italic.ttf"), 28)

# Networking
def request_theme():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 65432))
        s.sendall("GET_THEME".encode())
        data = s.recv(1024).decode()
        s.close()
        return json.loads(data)
    except:
        return {"name": "Error", "description": "Could not connect to server."}

# Button
button_width, button_height = 300, 60
button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - 30, button_width, button_height)

# States
current_theme = None
theme_selected = False
countdown_started = False
start_time = None
countdown_seconds = 5
game_started = False

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not theme_selected:
            if button_rect.collidepoint(event.pos):
                current_theme = request_theme()
                theme_selected = True
                countdown_started = True
                start_time = time.time()

    # Title
    title_text = title_font.render("Welcome to Catch The Look!", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

    # Button (only if theme not selected)
    if not theme_selected:
        pygame.draw.rect(screen, GREEN, button_rect, border_radius=12)
        btn_label = button_font.render("Randomize Theme", True, WHITE)
        screen.blit(btn_label, (
            button_rect.centerx - btn_label.get_width() // 2,
            button_rect.centery - btn_label.get_height() // 2
        ))

    # Theme Reveal
    if current_theme:
        name_text = theme_font.render(f"Theme: {current_theme['name']}", True, BLACK)
        desc_text = desc_font.render(current_theme['description'], True, BLACK)
        screen.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, HEIGHT // 2 + 90))
        screen.blit(desc_text, (WIDTH // 2 - desc_text.get_width() // 2, HEIGHT // 2 + 140))

    # Countdown
    if countdown_started and not game_started:
        elapsed = time.time() - start_time
        if elapsed < countdown_seconds:
            remaining = countdown_seconds - int(elapsed)
            countdown_text = theme_font.render(f"Starting in {remaining}...", True, PINK)
            screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 + 200))
        else:
            game_started = True

    # After countdown ends (placeholder for actual game)
    if game_started:
        start_msg = theme_font.render("Game Starting...", True, GREEN)
        screen.blit(start_msg, (WIDTH // 2 - start_msg.get_width() // 2, HEIGHT // 2 + 260))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
