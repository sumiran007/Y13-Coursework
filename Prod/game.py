import pygame
import ast
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox

class ChangingScreen:
    def __init__(self, width=800, height=600, sizew=50, sizeh=50, spacing=0, username="player"):
        pygame.init()
        self.username = username#stores who's playing
        self.start_y = 0
        self.width, self.height = width, height#screen dimensions
        self.sizew, self.sizeh = sizew, sizeh
        self.spacing = spacing
        self.camera_x, self.camera_y = 0, 0#starting camera position
        self.camera_speed_x, self.camera_speed_y = 0, -5#only moves up
        self.objects = []#empty list for all the squares
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.brown = (139, 69, 19)#for logs
        self.grey = (128, 128, 128)#for roads
        self.yellow = (255, 255, 0)#for the road lines
        
        self.obstacle_types = {
            'g': {'color': self.green, 'type': 'grass'},
            'r': {'color': self.grey, 'type': 'road'},
            'l': {'color': self.brown, 'type': 'log'},
            'w': {'color': self.blue, 'type': 'water'},
            's': {'color': self.black, 'type': 'stone'}
        }#matches letters to obstacle types and colors
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Frogger Game")
        self.clock = pygame.time.Clock()
        self.level_data = self.load_level_data("random_generations.txt")#opens the files with the pregenerated lists
        self.current_level = 0#
        
      #to get the game over int eh correct order and make sure it doesn't try draw anything after the game is over
        self.game_over = False
        self.game_over_message = ""

        self.sizew = self.width // 10#divides the screen width by 10
        self.sizeh = self.height // 10#divides the screen height by 10
        self.spacing = 0
        self.sizew = self.sizew - self.spacing

      #create the player sprite
        self.player_size = self.sizew // 2
        self.player = pygame.Rect(
            self.width // 2 - self.player_size // 2,
            self.height // 2 - self.player_size // 2,
            self.player_size, 
            self.player_size
        )#puts player in middle of screen
        
        self.player_speed = 5#movement speed of sprite
        self.gravity = 1#rate of screen moving out of reach

        self.add_squares(self.level_data[self.current_level], start_y=self.camera_y)#add the first set
        
        self.app = QApplication.instance()
        if not self.app:
            self.app = QApplication([])#needed for the popup message boxes

    def load_level_data(self, filepath):
        with open(filepath, "r") as file:
            level_data = [ast.literal_eval(line.strip()) for line in file]#reads the lists from file
        return level_data

    def add_squares(self, level_data, start_y=0):
        cols = int(self.width / self.sizew)#how many squares fit across screen
        for i, symbol in enumerate(level_data):
            x = (i % cols) * self.sizew#calculates x position
            y = start_y + (i // cols) * self.sizeh#calculates y position

            if symbol in self.obstacle_types:
                props = self.obstacle_types[symbol]
                self.objects.append({
                    "rect": pygame.Rect(x, y, self.sizew, self.sizeh), 
                    "color": props['color'],
                    "type": props['type']
                })#adds square to list with right properties

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False#quits when window closed
        
        keys = pygame.key.get_pressed()#gets all pressed keys
        moved = False
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.x -= self.player_speed#move left
            moved = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.x += self.player_speed#move right
            moved = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player.y -= self.player_speed * 2#move up faster to counter gravity
            moved = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player.y += self.player_speed#move down
            moved = True
            
      #apply "gravity" - player slowly falls down
        self.player.y += self.gravity
            
        if (self.player.left <= 0 or 
            self.player.right >= self.width or 
            self.player.top <= 0):
            
            self.game_over = True#hit edge of screen
            self.game_over_message = f"Game Over, {self.username}! You hit the edge of the screen."
            return False
            
        if self.player.bottom >= self.height:
            self.game_over = True#fell off bottom
            self.game_over_message = f"Game Over, {self.username}! You couldn't keep up with the treadmill!"
            return False
            
        return True

    def update_camera(self):
        self.camera_y += self.camera_speed_y#moves camera up

        while len(self.objects) == 0 or self.objects[-1]["rect"].top > self.camera_y:
            self.add_squares(self.level_data[self.current_level], start_y=self.camera_y - self.sizeh)#adds more squares as needed

        self.objects = [obj for obj in self.objects if obj["rect"].top < self.camera_y + self.height]#removes squares that scrolled off screen

        if self.camera_y < -self.height * (self.current_level + 1):
            self.current_level = (self.current_level + 1) % len(self.level_data)#cycles to next level

    def draw(self):
        self.screen.fill(self.white)#blank screen
        
        for obj in self.objects:
            rect = obj["rect"].move(-self.camera_x, -self.camera_y)#adjusts position for camera
            pygame.draw.rect(self.screen, obj["color"], rect)#draws the square
            
            if obj["type"] == "road":
                line_width = 4
                dash_length = self.sizew // 3
                gap_length = self.sizew // 6
                
                y_middle = rect.top + rect.height // 2 - line_width // 2#center of road
                x_start = rect.left
                while x_start < rect.right:
                    pygame.draw.rect(self.screen, self.yellow, 
                                    (x_start, y_middle, min(dash_length, rect.right - x_start), line_width))#draws dashed yellow line
                    x_start += dash_length + gap_length#spaces out dashes
        
        pygame.draw.rect(self.screen, self.black, self.player)#draws player
        
        font = pygame.font.Font(None, 24)
        score = abs(int(self.camera_y))
        debug_text = font.render(f"Score: {score} | Camera Y: {self.camera_y}", True, self.black)#score and debug info
        self.screen.blit(debug_text, (10, 10))#shows text at top
        
        pygame.display.flip()#updates screen

    def run(self):
        running = True
        while running:
            running = self.handle_events()#check input
            if running:
                self.update_camera()#move camera
                self.draw()#draw everything
            self.clock.tick(30)#limits to 30 fps
            
        if self.game_over:
            pygame.quit()
            msg_box = QMessageBox()#creates popup
            msg_box.setWindowTitle("Game Over")
            msg_box.setText(self.game_over_message)#shows game over reason
            msg_box.exec_()#shows the popup
        else:
            pygame.quit()#just quits


def main(username="player"):
    game = ChangingScreen(username=username)#creates game
    game.run()#starts game loop


if __name__ == "__main__":
    username = "player"#default name
    if len(sys.argv) > 1:
        username = sys.argv[1]#use command line argument if given
    main(username)#starts game