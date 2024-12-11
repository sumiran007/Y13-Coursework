import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()

<<<<<<< HEAD
# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Automatic Camera Panning")

# Game world dimensions
WORLD_WIDTH, WORLD_HEIGHT = 1600, 1200

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)

# Camera position and speed
camera_x, camera_y = 0, 0
camera_speed_x, camera_speed_y = 2, 1  # Speed of camera panning in x and y directions

# Dummy objects to display in the game world
objects = [pygame.Rect(x * 100, y * 100, 50, 50) for x in range(16) for y in range(12)]

# Game loop
=======

sizew, sizeh = 800, 600
screen = pygame.display.set_mode((sizew, sizeh))
pygame.display.set_caption("Automatic Camera Panning")


width = 1000
height = 100000


white = (255, 255, 255)
green = (0, 200, 0)


camera_x, camera_y = 0, 0
camera_speed_x, camera_speed_y = 0, -2

squarew = width//2
squarew = height//2
objects = [pygame.Rect(x * 100, y * 100, 50, 50) for x in range(squarew) for y in range(12)]


>>>>>>> 2afc89b (some changes to campan.py to increase the space and the number of squares generated to keep it in line with actual crossy road/ frogger)
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Update camera position automatically
    camera_x += camera_speed_x
    camera_y += camera_speed_y

    # Keep camera within world bounds
<<<<<<< HEAD
    if camera_x < 0 or camera_x > WORLD_WIDTH - SCREEN_WIDTH:
        camera_speed_x = -camera_speed_x  # Reverse direction
    if camera_y < 0 or camera_y > WORLD_HEIGHT - SCREEN_HEIGHT:
        camera_speed_y = -camera_speed_y  # Reverse direction

    # Drawing
    screen.fill(WHITE)

    # Draw objects relative to the camera
    for obj in objects:
        pygame.draw.rect(screen, GREEN, obj.move(-camera_x, -camera_y))

=======
    if camera_x < 0 or camera_x > width - sizew:
        camera_speed_x = -camera_speed_x  # Reverse direction
    if camera_y < 0 or camera_y > height - sizeh:
        camera_speed_y = -camera_speed_y  

    # Drawing
    screen.fill(white)

    # Draw objects relative to the camera
    for obj in objects:
        pygame.draw.rect(screen, green, obj.move(-camera_x, -camera_y))
 
>>>>>>> 2afc89b (some changes to campan.py to increase the space and the number of squares generated to keep it in line with actual crossy road/ frogger)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
