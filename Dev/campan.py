import pygame

def initialize():
    pygame.init()
    width, height = 1000, 1000
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Camera Pan Example")
    clock = pygame.time.Clock()
    return screen, clock, width, height

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

def update_camera(camera_x, camera_y, camera_speed_x, camera_speed_y, width, height, sizew, sizeh):
    camera_x += camera_speed_x
    camera_y += camera_speed_y

    if camera_x < 0 or camera_x > width - sizew:
        camera_speed_x = -camera_speed_x
    if camera_y < 0 or camera_y > height - sizeh:
        camera_speed_y = -camera_speed_y

    return camera_x, camera_y, camera_speed_x, camera_speed_y

def draw(screen, white, green, objects, camera_x, camera_y):
    screen.fill(white)
    for obj in objects:
        pygame.draw.rect(screen, green, obj.move(-camera_x, -camera_y))
    pygame.display.flip()

def main():
    screen, clock, width, height = initialize()
    white = (255, 255, 255)
    green = (0, 255, 0)
    sizew, sizeh = 50, 50
    camera_x, camera_y = 0, 0
    camera_speed_x, camera_speed_y = 5, 5
    objects = [pygame.Rect(100, 100, sizew, sizeh), pygame.Rect(300, 300, sizew, sizeh)]

    running = True
    while running:
        running = handle_events()
        camera_x, camera_y, camera_speed_x, camera_speed_y = update_camera(camera_x, camera_y, camera_speed_x, camera_speed_y, width, height, sizew, sizeh)
        draw(screen, white, green, objects, camera_x, camera_y)
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()