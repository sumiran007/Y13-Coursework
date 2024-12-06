import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Camera Panning Example")

# Game world dimensions
WORLD_WIDTH, WORLD_HEIGHT = 1600, 1600

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)

# Camera position
camera_x, camera_y = 0, 0
camera_speed = 10

# Dummy objects to display in the game world
objects = [pygame.Rect(x * 100, y * 100, 50, 50) for x in range(WORLD_WIDTH//10) for y in range(WORLD_HEIGHT // 100)]

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Get pressed keys
    keys = pygame.key.get_pressed()
    if keys[K_w]:
        camera_y = max(camera_y - camera_speed, 0)
    if keys[K_s]:
        camera_y = min(camera_y + camera_speed, WORLD_HEIGHT - SCREEN_HEIGHT)
    if keys[K_a]:
        camera_x = max(camera_x - camera_speed, 0)
    if keys[K_d]:
        camera_x = min(camera_x + camera_speed, WORLD_WIDTH - SCREEN_WIDTH)

    # Drawing
    screen.fill(WHITE)

    # Draw objects relative to the camera
    for obj in objects:
        pygame.draw.rect(screen, GREEN, obj.move(-camera_x, -camera_y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
