import pygame
import ast
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox

class ChangingScreen:
    def __init__(self, width=800, height=600, sizew=50, sizeh=50, spacing=0, username="player"):
        pygame.init()
        self.username = username
        self.start_y = 0
        self.width, self.height = width, height
        self.sizew, self.sizeh = sizew, sizeh
        self.spacing = spacing
        self.camera_x, self.camera_y = 0, 0
        self.camera_speed_x, self.camera_speed_y = 0, -5
        self.objects = []
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.brown = (139, 69, 19)
        self.black = (0, 0, 0)
        self.grey = (128, 128, 128)
        self.yellow = (255, 255, 0)
        
        self.obstacle_types = {
            'g': {'color': self.green, 'type': 'grass'},
            'r': {'color': self.grey, 'type': 'road'},
            'l': {'color': self.brown, 'type': 'log'},
            'w': {'color': self.blue, 'type': 'water'},
            's': {'color': self.black, 'type': 'stone'}
        }
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Frogger Game")
        self.clock = pygame.time.Clock()
        self.level_data = self.load_level_data("random_generations.txt")  #opens the files with the pregenerated lists
        self.current_level = 0  #
        
        #to get the game over int eh correct order and make sure it doesn't try draw anything after the game is over
        self.game_over = False
        self.game_over_message = ""

        self.sizew = self.width // 10  #divides the screen width by 10
        self.sizeh = self.height // 10  #divides the screen height by 10
        self.spacing = 0
        self.sizew = self.sizew - self.spacing

        #create the player sprite
        self.player_size = self.sizew // 2
        self.player = pygame.Rect(
            self.width // 2 - self.player_size // 2,
            self.height // 2 - self.player_size // 2,
            self.player_size, 
            self.player_size
        )
        
        self.player_speed = 5  #movement speed of sprite
        self.gravity = 1  #rate of screen moving out of reach

        self.add_squares(self.level_data[self.current_level], start_y=self.camera_y)  # add the first set
        
        self.app = QApplication.instance()
        if not self.app:
            self.app = QApplication([])

    def load_level_data(self, filepath):
        with open(filepath, "r") as file:
            level_data = [ast.literal_eval(line.strip()) for line in file]
        return level_data

    def add_squares(self, level_data, start_y=0):
        cols = int(self.width / self.sizew)
        for i, symbol in enumerate(level_data):
            x = (i % cols) * self.sizew
            y = start_y + (i // cols) * self.sizeh

            if symbol in self.obstacle_types:
                props = self.obstacle_types[symbol]
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
        moved = False
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.x -= self.player_speed
            moved = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.x += self.player_speed
            moved = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player.y -= self.player_speed * 2  # Move up faster to counter gravity
            moved = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player.y += self.player_speed
            moved = True
            
        #apply "gravity" - player slowly falls down
        self.player.y += self.gravity
            
        if (self.player.left <= 0 or 
            self.player.right >= self.width or 
            self.player.top <= 0):
            
            self.game_over = True
            self.game_over_message = f"Game Over, {self.username}! You hit the edge of the screen."
            return False
            
        if self.player.bottom >= self.height:
            self.game_over = True
            self.game_over_message = f"Game Over, {self.username}! You couldn't keep up with the treadmill!"
            return False
            
        return True

    def update_camera(self):
        self.camera_y += self.camera_speed_y

        while len(self.objects) == 0 or self.objects[-1]["rect"].top > self.camera_y:
            self.add_squares(self.level_data[self.current_level], start_y=self.camera_y - self.sizeh)

        self.objects = [obj for obj in self.objects if obj["rect"].top < self.camera_y + self.height]

        if self.camera_y < -self.height * (self.current_level + 1):
            self.current_level = (self.current_level + 1) % len(self.level_data)

    def draw(self):
        self.screen.fill(self.white)
        
        for obj in self.objects:
            rect = obj["rect"].move(-self.camera_x, -self.camera_y)
            pygame.draw.rect(self.screen, obj["color"], rect)
            
            if obj["type"] == "road":
                line_width = 4
                dash_length = self.sizew // 3
                gap_length = self.sizew // 6
                
                y_middle = rect.top + rect.height // 2 - line_width // 2
                x_start = rect.left
                while x_start < rect.right:
                    pygame.draw.rect(self.screen, self.yellow, 
                                    (x_start, y_middle, min(dash_length, rect.right - x_start), line_width))
                    x_start += dash_length + gap_length
        
        pygame.draw.rect(self.screen, self.black, self.player)
        
        font = pygame.font.Font(None, 24)
        score = abs(int(self.camera_y))
        debug_text = font.render(f"Score: {score} | Camera Y: {self.camera_y}", True, self.black)
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
            
        if self.game_over:
            pygame.quit()
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Game Over")
            msg_box.setText(self.game_over_message)
            msg_box.exec_()
        else:
            pygame.quit()


def main(username="player"):
    game = ChangingScreen(username=username)
    game.run()


if __name__ == "__main__":
    username = "player"
    if len(sys.argv) > 1:
        username = sys.argv[1]
    main(username)