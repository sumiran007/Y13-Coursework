import pygame

def initialize():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    clock = pygame.time.Clock()
    return screen, player_pos, clock
#this uses a while loop ot check whether the x is clicked to close the window
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

def update():
    pass  # Add game state updates here if needed
#function that renders the looks of the window
def render(screen, player_pos):
    screen.fill("purple")
    pygame.draw.circle(screen, "green", player_pos, 40)
    pygame.display.flip()
#main function that runs the game
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
#runs when the script is run and not when it is imported as a module
if __name__ == "__main__":
    main()