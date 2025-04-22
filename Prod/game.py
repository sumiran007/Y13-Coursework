import pygame
import ast
import sys
import os
import random  #need this for the random terrain stuff
from PyQt5.QtWidgets import QApplication, QMessageBox

class ChangingScreen:
    def __init__(self, width=800, height=600, sizew=50, sizeh=50, spacing=0, username="player"):
        pygame.init()
        self.username = username#keeps track of who's playing
        self.start_y = 0
        self.width, self.height = width, height#how big the game window is
        self.sizew, self.sizeh = sizew, sizeh
        self.spacing = spacing
        self.camera_x, self.camera_y = 0, 0#where the camera starts
        self.camera_speed_x, self.camera_speed_y = 0, -5#only goes up
        self.objects = []#empty list for all the squares
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.brown = (139, 69, 19)#for the logs
        self.black = (0, 0, 0)
        self.grey = (128, 128, 128)#for roads
        self.yellow = (255, 255, 0)#for the yellow lines on roads
        
        #try to grab the log image
        try:
            self.log_image = pygame.image.load("assets/log.png")  #log pic
            self.log_image = pygame.transform.scale(self.log_image, (self.sizew, self.sizeh))
        except pygame.error:
            print("Couldn't find log image. Using boring brown rectangle instead.")
            self.log_image = None
        
        self.obstacle_types = {
            'g': {'color': self.green, 'type': 'grass'},
            'r': {'color': self.grey, 'type': 'road'},
            'l': {'color': self.brown, 'type': 'log'},
            'w': {'color': self.blue, 'type': 'water'},
            's': {'color': self.black, 'type': 'stone'}
        }#links letters to obstacle types and colors
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Frogger Game")
        self.clock = pygame.time.Clock()
        
        #grab the level patterns from file
        file_path = "random_generations.txt"
        if os.path.exists(file_path):
            self.level_data = self.load_level_data(file_path)
            random.shuffle(self.level_data)
            self.next_rows = self.level_data[:20]
            self.level_data = self.level_data[20:] if len(self.level_data) > 20 else []
        else:
            print("Oops! Can't find random_generations.txt!")
            pygame.quit()
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Error")
            msg_box.setText("Can't find level data file. Make sure 'random_generations.txt' exists.")
            msg_box.exec_()
            sys.exit(1)
        
        self.game_over = False
        self.game_over_message = ""

        self.sizew = self.width // 10#splits screen into 10 columns
        self.sizeh = self.height // 10#splits screen into 10 rows
        self.spacing = 0
        self.sizew = self.sizew - self.spacing

        self.player_size = self.sizew // 2
        self.player = pygame.Rect(
            self.width // 2 - self.player_size // 2,
            self.height // 2 - self.player_size // 2,
            self.player_size, 
            self.player_size
        )#sticks player in middle of screen
        
        self.player_speed = 5#how fast player moves

        self.add_initial_rows()
        
        self.app = QApplication.instance()
        if not self.app:
            self.app = QApplication([])#needed for popup messages

    def load_level_data(self, filepath):
        try:
            with open(filepath, "r") as file:
                level_data = [ast.literal_eval(line.strip()) for line in file]#pulls lists from file
            return level_data
        except Exception as e:
            print(f"Ugh, problem loading level data: {e}")
            return []

    def add_initial_rows(self):
        start_y = self.camera_y
        for i, terrain_list in enumerate(self.next_rows):
            y = start_y + i * self.sizeh
            self.add_patterned_row(terrain_list, y)

    def add_patterned_row(self, terrain_list, y):
        cols = int(self.width / self.sizew)
        
        if len(terrain_list) > cols:
            terrain_list = terrain_list[:cols]
        
        while len(terrain_list) < cols:
            terrain_list.append(terrain_list[-1])
        
        for col, terrain in enumerate(terrain_list):
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
                return False#quits when player closes window
        
        keys = pygame.key.get_pressed()#checks all keyboard inputs
        moved = False
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.x -= self.player_speed#go left
            moved = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.x += self.player_speed#go right
            moved = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player.y -= self.player_speed#go up (normal speed vs screen scroll)
            moved = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player.y += self.player_speed#go down
            moved = True
            
        if (self.player.left <= 0 or 
            self.player.right >= self.width or 
            self.player.top <= 0):
            
            self.game_over = True#hit edge of screen = dead
            self.game_over_message = f"Game Over, {self.username}! You hit the edge of the screen."
            return False
            
        if self.player.bottom >= self.height:
            self.game_over = True#fell off bottom = dead
            self.game_over_message = f"Game Over, {self.username}! Too slow - keep up with the screen!"
            return False
            
        return True

    def update_camera(self):
        try:
            previous_camera_y = self.camera_y#remember where camera was
            self.camera_y += self.camera_speed_y#move camera up
            
            camera_change = self.camera_y - previous_camera_y
            self.player.y -= camera_change#keeps player in same relative spot

            if len(self.objects) == 0 or self.objects[-1]["rect"].top > self.camera_y:
                top_y = self.camera_y - self.sizeh

                for i, terrain_list in enumerate(self.next_rows):
                    y = top_y - (i * self.sizeh)
                    self.add_patterned_row(terrain_list, y)
                
                if hasattr(self, 'level_data') and self.level_data:
                    self.next_rows = self.level_data[:20]
                    self.level_data = self.level_data[20:] if len(self.level_data) > 20 else []
                else:
                    file_path = "random_generations.txt"
                    if os.path.exists(file_path):
                        self.level_data = self.load_level_data(file_path)
                        random.shuffle(self.level_data)
                        self.next_rows = self.level_data[:20]
                        self.level_data = self.level_data[20:] if len(self.level_data) > 20 else []
                    else:
                        print("Oops! Lost the level data file during gameplay!")
                        self.game_over = True
                        self.game_over_message = f"Game Over, {self.username}! Level data went missing."

            max_objects = 1000
            if len(self.objects) > max_objects:
                self.objects = self.objects[-max_objects:]

            self.objects = [obj for obj in self.objects if obj["rect"].top < self.camera_y + self.height]#ditches objects that scrolled off screen
            
        except Exception as e:
            print(f"Whoops! Camera update error: {e}")

    def draw(self):
        try:
            self.screen.fill(self.white)#clear screen
            
            for obj in self.objects:
                rect = obj["rect"].move(-self.camera_x, -self.camera_y)#adjust for camera position
                
                if obj["type"] == "log" and hasattr(self, 'log_image') and self.log_image:
                    self.screen.blit(self.log_image, rect)  #use log pic
                else:
                    pygame.draw.rect(self.screen, obj["color"], rect)#draw the square
                
                if obj["type"] == "road":
                    line_width = 4
                    dash_length = self.sizew // 3
                    gap_length = self.sizew // 6
                    
                    y_middle = rect.top + rect.height // 2 - line_width // 2#center of road
                    x_start = rect.left
                    while x_start < rect.right:
                        pygame.draw.rect(self.screen, self.yellow, 
                                        (x_start, y_middle, min(dash_length, rect.right - x_start), line_width))#make dashed yellow line
                        x_start += dash_length + gap_length#space between dashes
            
            pygame.draw.rect(self.screen, self.black, self.player)#draw player
            
            font = pygame.font.Font(None, 24)
            score = abs(int(self.camera_y))
            debug_text = font.render(f"Score: {score} | Camera Y: {self.camera_y}", True, self.black)#show score and camera y
            self.screen.blit(debug_text, (10, 10))#put text at top
            
            pygame.display.flip()#update display
        except Exception as e:
            print(f"Drawing glitch: {e}")

    def run(self):
        running = True
        frame_count = 0
        try:
            while running:
                frame_count += 1
                if frame_count % 300 == 0:  #show debug every 300 frames
                    print(f"Frame {frame_count}, Camera Y: {self.camera_y}, Objects: {len(self.objects)}")
                
                running = self.handle_events()#check inputs
                if running:
                    self.update_camera()#move camera
                    self.draw()#draw everything
                self.clock.tick(30)#cap at 30fps
                
        except Exception as e:
            print(f"Game loop crashed: {e}")
            
        if self.game_over:
            pygame.quit()#quit for game over message
            msg_box = QMessageBox()#make popup
            msg_box.setWindowTitle("Game Over")
            msg_box.setText(self.game_over_message)#show why game ended
            msg_box.exec_()#display popup
        else:
            pygame.quit()#just quit


def main(username="player"):
    try:
        game = ChangingScreen(username=username)#create game
        game.run()#fire it up
    except Exception as e:  
        print(f"Big problem: {e}")
        pygame.quit()


if __name__ == "__main__":
    username = "player"#default name
    if len(sys.argv) > 1:
        username = sys.argv[1]#use command line arg if given
    main(username)#start the game