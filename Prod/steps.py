import pygame
import sys
import random

class ChangingScreen:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Frogger Game")
        self.clock = pygame.time.Clock()
        
        self.player = pygame.Rect(
            self.width // 2 - 25,
            self.height // 2 - 25,
            50, 50
        )  #player in middle of screen
        
        self.player_speed = 5
        
        self.camera_y = 0
        self.camera_speed_y = -5  #camera moves up
        
        self.objects = []
        self.sizew = width // 10
        self.sizeh = height // 10
        
        self.green = (0, 255, 0)  # Grass
        self.blue = (0, 0, 255)   # Water
        self.grey = (128, 128, 128)  # Road
        self.yellow = (255, 255, 0)  # Road lines
        
        # Fixed data structure
        self.obstacle_types = {
            'g': {'color': self.green, 'type': 'grass'},
            'w': {'color': self.blue, 'type': 'water'},
            'r': {'color': self.grey, 'type': 'road'}
        }
        
        self.game_over = False
        
        self.next_rows = [['g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g']]
        self.add_initial_rows()
    
    def add_initial_rows(self):
        start_y = self.camera_y
        for i, row in enumerate(self.next_rows):
            y = start_y + i * self.sizeh
            self.add_row(row, y)
    
    def add_row(self, row, y):
        for col, terrain in enumerate(row):
            if terrain in self.obstacle_types:
                props = self.obstacle_types[terrain]
                x = col * self.sizew
                self.objects.append({
                    "rect": pygame.Rect(x, y, self.sizew, self.sizeh),
                    "color": props['color'],
                    "type": props['type']
                })
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        
        keys = pygame.key.get_pressed()
        moved = False  # Track if player moved this frame
        
        if keys[pygame.K_LEFT]:
            self.player.x -= self.player_speed
            moved = True
        if keys[pygame.K_RIGHT]:
            self.player.x += self.player_speed
            moved = True
        if keys[pygame.K_UP]:
            self.player.y -= self.player_speed
            moved = True
        if keys[pygame.K_DOWN]:
            self.player.y += self.player_speed
            moved = True
        
        # THE BUG: This doesn't account for camera movement pushing player down!
        # If player doesn't move, they might still hit screen edge due to camera
        # Also, we don't reset player position like we should 
        if (self.player.left < 0 or
            self.player.right > self.width or
            self.player.top < 0 or
            self.player.bottom > self.height):
            
            # Instead of stopping at border, we just end the game
            if not moved:  # Only game over if player didn't move this frame
                self.game_over = True
                return False
            
            # This means if camera pushes player off-screen, they die
            # even though they didn't have a chance to react
        
        return True
    
    def update_camera(self):
        previous_camera_y = self.camera_y
        self.camera_y += self.camera_speed_y
        
        # Keep player in the same relative position
        camera_change = self.camera_y - previous_camera_y
        self.player.y -= camera_change
    
    def draw(self):
        self.screen.fill((255, 255, 255))
        
        # Now we can check object types properly
        for obj in self.objects:
            rect = obj["rect"].move(0, -self.camera_y)
            pygame.draw.rect(self.screen, obj["color"], rect)
            
            # Add yellow lines to roads
            if obj["type"] == "road":
                # Draw yellow lines
                line_width = 4
                y_middle = rect.top + rect.height // 2 - line_width // 2
                pygame.draw.rect(self.screen, self.yellow, 
                               (rect.left, y_middle, rect.width, line_width))
        
        pygame.draw.rect(self.screen, (0, 0, 0), 
                        self.player)
        
        # Add debug info
        font = pygame.font.Font(None, 24)
        debug_text = font.render(f"Player pos: {self.player.y}, Camera: {self.camera_y}", True, (0, 0, 0))
        self.screen.blit(debug_text, (10, 10))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            if running:
                self.update_camera()
                self.draw()
            self.clock.tick(30)
        pygame.quit()
        
        if self.game_over:
            print("Game Over! You fell off the screen!")

if __name__ == "__main__":
    game = ChangingScreen()
    game.run()