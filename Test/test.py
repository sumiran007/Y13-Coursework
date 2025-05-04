import pygame
import sys

def main(username="player", skin_name=None):
    #pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    dt = 0
    
    # Display username on window title
    pygame.display.set_caption(f"Game - Player: {username}")
    
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    
    # You could use skin_name to change player appearance
    player_color = "red"
    if skin_name == "blue":
        player_color = "blue"
    elif skin_name == "green":
        player_color = "green"

    while running:
        #poll for events
        #pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")

        pygame.draw.circle(screen, player_color, player_pos, 40)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player_pos.y -= 300 * dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player_pos.y += 300 * dt
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player_pos.x -= 300 * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player_pos.x += 300 * dt

        #flip() the display to put your work on screen
        pygame.display.flip()

        #limits FPS to 60
        #dt is delta time in seconds since last frame, used for framerate-
        #independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()

# Direct execution block without using if __name__ == "__main__":
username = "player"
skin_name = None

# Check command line arguments
if len(sys.argv) > 1:
    username = sys.argv[1]

if len(sys.argv) > 2:
    skin_name = sys.argv[2]

# Run the main function
main(username, skin_name)