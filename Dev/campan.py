import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()


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
    if camera_x < 0 or camera_x > width - sizew:
        camera_speed_x = -camera_speed_x  # Reverse direction
    if camera_y < 0 or camera_y > height - sizeh:
        camera_speed_y = -camera_speed_y  

    # Drawing
    screen.fill(white)

    # Draw objects relative to the camera
    for obj in objects:
        pygame.draw.rect(screen, green, obj.move(-camera_x, -camera_y))
 
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
