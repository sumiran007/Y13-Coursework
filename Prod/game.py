import pygame
import ast
import sys
import os
import random  # Add this for random terrain generation
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
        self.black = (0, 0, 0)
        self.grey = (128, 128, 128)#for roads
        self.yellow = (255, 255, 0)#for the road lines
        
        # Load the log image
        try:
            self.log_image = pygame.image.load("assets/log.png")  # Save the image as log.png
            self.log_image = pygame.transform.scale(self.log_image, (self.sizew, self.sizeh))
        except pygame.error:
            print("Could not load log image. Using default brown rectangle.")
            self.log_image = None
        
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
        
        # Try to load patterns from file
        file_path = "random_generations.txt"
        if os.path.exists(file_path):
            self.level_data = self.load_level_data(file_path)
            # Shuffle the level data to randomize the order
            random.shuffle(self.level_data)
            self.next_rows = self.level_data[:20]
            self.level_data = self.level_data[20:] if len(self.level_data) > 20 else []
        else:
            # Display error message and exit if file doesn't exist
            print("Error: random_generations.txt file not found!")
            pygame.quit()
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Error")
            msg_box.setText("Level data file not found. Please make sure 'random_generations.txt' exists.")
            msg_box.exec_()
            sys.exit(1)
        
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

        # Add the first set of rows
        self.add_initial_rows()
        
        self.app = QApplication.instance()
        if not self.app:
            self.app = QApplication([])#needed for the popup message boxes

    def load_level_data(self, filepath):
        """Load terrain patterns from file"""
        try:
            with open(filepath, "r") as file:
                level_data = [ast.literal_eval(line.strip()) for line in file]#reads the lists from file
            return level_data
        except Exception as e:
            print(f"Error loading level data: {e}")
            return []

    def add_initial_rows(self):
        """Add the initial rows to the screen"""
        start_y = self.camera_y
        for i, terrain_list in enumerate(self.next_rows):
            y = start_y + i * self.sizeh
            self.add_patterned_row(terrain_list, y)

    def add_patterned_row(self, terrain_list, y):
        """Add a row with the terrain pattern exactly as specified in the list"""
        cols = int(self.width / self.sizew)
        
        # Make sure we don't have more elements than columns
        if len(terrain_list) > cols:
            terrain_list = terrain_list[:cols]
        
        # If the list is shorter than the number of columns, repeat the last element
        while len(terrain_list) < cols:
            terrain_list.append(terrain_list[-1])
        
        # Add each terrain square according to the pattern in the list
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
            self.player.y -= self.player_speed#move up (normal speed, no need to counter gravity)
            moved = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player.y += self.player_speed#move down
            moved = True
            
        if (self.player.left <= 0 or 
            self.player.right >= self.width or 
            self.player.top <= 0):
            
            self.game_over = True#hit edge of screen
            self.game_over_message = f"Game Over, {self.username}! You hit the edge of the screen."
            return False
            
        if self.player.bottom >= self.height:
            self.game_over = True#fell off bottom
            self.game_over_message = f"Game Over, {self.username}! You couldn't keep up with the scrolling!"
            return False
            
        return True

    def update_camera(self):
        try:
            previous_camera_y = self.camera_y#store previous camera position
            self.camera_y += self.camera_speed_y#moves camera up
            
            # Move player along with camera to keep them on the same tile
            camera_change = self.camera_y - previous_camera_y
            self.player.y -= camera_change#this keeps player on same relative position

            # Check if we need to add more rows
            if len(self.objects) == 0 or self.objects[-1]["rect"].top > self.camera_y:
                # Get the top-most row position
                top_y = self.camera_y - self.sizeh

                # Add new rows from our pre-generated list
                for i, terrain_list in enumerate(self.next_rows):
                    y = top_y - (i * self.sizeh)
                    self.add_patterned_row(terrain_list, y)
                
                # Get more rows from the file if available, otherwise loop back to the beginning
                if hasattr(self, 'level_data') and self.level_data:
                    self.next_rows = self.level_data[:20]
                    self.level_data = self.level_data[20:] if len(self.level_data) > 20 else []
                else:
                    # If we've used all file data, reload and shuffle
                    file_path = "random_generations.txt"
                    if os.path.exists(file_path):
                        self.level_data = self.load_level_data(file_path)
                        # Shuffle again for more randomness
                        random.shuffle(self.level_data)
                        self.next_rows = self.level_data[:20]
                        self.level_data = self.level_data[20:] if len(self.level_data) > 20 else []
                    else:
                        print("Error: Level data file not found during gameplay!")
                        self.game_over = True
                        self.game_over_message = f"Game Over, {self.username}! Level data could not be loaded."

            # Limit the number of objects to prevent memory issues
            max_objects = 1000
            if len(self.objects) > max_objects:
                self.objects = self.objects[-max_objects:]  # Keep only the most recent objects

            # Clean up off-screen objects
            self.objects = [obj for obj in self.objects if obj["rect"].top < self.camera_y + self.height]#removes squares that scrolled off screen
            
        except Exception as e:
            print(f"Error in update_camera: {e}")

    def draw(self):
        try:
            self.screen.fill(self.white)#blank screen
            
            for obj in self.objects:
                rect = obj["rect"].move(-self.camera_x, -self.camera_y)#adjusts position for camera
                
                # Check if it's a log and we have the log image
                if obj["type"] == "log" and hasattr(self, 'log_image') and self.log_image:
                    self.screen.blit(self.log_image, rect)  # Draw log image
                else:
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
        except Exception as e:
            print(f"Error in draw method: {e}")

    def run(self):
        running = True
        frame_count = 0
        try:
            while running:
                frame_count += 1
                if frame_count % 300 == 0:  # Print debug info every 300 frames
                    print(f"Frame {frame_count}, Camera Y: {self.camera_y}, Objects: {len(self.objects)}")
                
                running = self.handle_events()#check input
                if running:
                    self.update_camera()#move camera
                    self.draw()#draw everything
                self.clock.tick(30)#limits to 30 fps
                
        except Exception as e:
            print(f"Error in game loop: {e}")
            
        if self.game_over:
            pygame.quit()#this is for the game over message
            msg_box = QMessageBox()#creates popup
            msg_box.setWindowTitle("Game Over")
            msg_box.setText(self.game_over_message)#shows game over reason
            msg_box.exec_()#shows the popup
        else:
            pygame.quit()#just quits


def main(username="player"):
    try:
        game = ChangingScreen(username=username)#creates game
        game.run()#starts game loop
    except Exception as e:  
        print(f"Critical error: {e}")
        pygame.quit()


if __name__ == "__main__":
    username = "player"#default name
    if len(sys.argv) > 1:
        username = sys.argv[1]#use command line argument if given
    main(username)#starts game