import pygame

class ChangingScreen:
    def __init__(self, width=800, height=600, sizew=50, sizeh=50):
        pygame.init()
        self.width, self.height = width, height
        self.sizew, self.sizeh = sizew, sizeh
        self.camera_x, self.camera_y = 0, 0
        self.camera_speed_x, self.camera_speed_y = 5, 5
        self.objects = [pygame.Rect(100, 100, sizew, sizeh), pygame.Rect(300, 300, sizew, sizeh)]
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Camera Pan Example")
        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def update_camera(self):
        self.camera_x += self.camera_speed_x
        self.camera_y += self.camera_speed_y

        if self.camera_x < 0 or self.camera_x > self.width - self.sizew:
            self.camera_speed_x = -self.camera_speed_x
        if self.camera_y < 0 or self.camera_y > self.height - self.sizeh:
            self.camera_speed_y = -self.camera_speed_y

    def draw(self):
        self.screen.fill(self.white)
        for obj in self.objects:
            pygame.draw.rect(self.screen, self.green, obj.move(-self.camera_x, -self.camera_y))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update_camera()
            self.draw()
            self.clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    game = ChangingScreen()
    game.run()