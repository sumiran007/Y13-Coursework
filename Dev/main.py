import pygame

def initialize():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    clock = pygame.time.Clock()
    return screen, player_pos, clock

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

def update():
    pass  # Add game state updates here if needed

def render(screen, player_pos):
    screen.fill("purple")
    pygame.draw.circle(screen, "green", player_pos, 40)
    pygame.display.flip()

def main():
    screen, player_pos, clock = initialize()
    fps = 60
    running = True

    while running:
        running = handle_events()
        update()
        render(screen, player_pos)
        clock.tick(fps)
    
    pygame.quit()

main()  # Call main directly