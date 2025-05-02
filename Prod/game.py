import pygame
import ast
import sys
import os
import random
import json
from PyQt5.QtWidgets import QApplication, QMessageBox

class ChangingScreen:
    def __init__(self, width=800, height=600, sizew=50, sizeh=50, spacing=0, username="player", skin_name=None):
        pygame.init()
        self.username = username
        self.skin_name = skin_name
        self.player_image = None

        self.start_y = 0
        self.width, self.height = width, height

        #calculate grid sizes
        self.sizew = self.width // 10
        self.sizeh = self.height // 10
        self.spacing = 0
        self.sizew = self.sizew - self.spacing

        self.camera_x, self.camera_y = 0, 0
        self.camera_speed_x, self.camera_speed_y = 0, -3  #slowed down camera speed
        self.objects = []
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.brown = (139, 69, 19)
        self.black = (0, 0, 0)
        self.grey = (128, 128, 128)
        self.yellow = (255, 255, 0)

        #add game timer for tracking elapsed time
        self.game_start_time = pygame.time.get_ticks()

        #try to grab the log image
        try:
            self.log_image = pygame.image.load("assets/log.png")
            self.log_image = pygame.transform.scale(self.log_image, (self.sizew, self.sizeh))
        except pygame.error:
            print("Couldn't find log image. Using boring brown rectangle instead.")
            self.log_image = None

        #try to grab the truck image
        try:
            self.truck_image = pygame.image.load("assets/truck.png")
            self.truck_image = pygame.transform.scale(self.truck_image, (self.sizew * 2, self.sizeh))
        except pygame.error:
            print("Couldn't find truck image. Using a red rectangle instead.")
            self.truck_image = None

        #load the player skin if one is specified
        self.load_player_skin()

        self.obstacle_types = {
            'g': {'color': self.green, 'type': 'grass'},
            'r': {'color': self.grey, 'type': 'road'},
            'l': {'color': self.brown, 'type': 'log'},
            'w': {'color': self.blue, 'type': 'water'},
            's': {'color': self.black, 'type': 'stone'},
            't': {'color': self.red, 'type': 'truck'}
        }

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Frogger Game")
        self.clock = pygame.time.Clock()

        #grab the level patterns from file
        file_path = "random_generations.txt"
        if os.path.exists(file_path):
            self.level_data = self.load_level_data(file_path)
            random.shuffle(self.level_data)
            
            # Force the first 10 rows to be grass
            self.next_rows = []
            for _ in range(10):
                self.next_rows.append(['g'] * 10)  # 10 grass rows
            
            # Add more rows from level data after the grass section
            for i in range(10):
                if i < len(self.level_data):
                    self.next_rows.append(self.level_data[i])
            
            self.level_data = self.level_data[10:] if len(self.level_data) > 10 else []
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

        self.player_size = self.sizew // 2
        self.player = pygame.Rect(
            self.width // 2 - self.player_size // 2,
            self.height // 2 - self.player_size // 2,
            self.player_size,
            self.player_size
        )

        self.player_speed = 10  #increased player speed

        self.add_initial_rows()

        #ensure the player does not start overlapping with a truck
        for obj in self.objects:
            if obj["type"] == "truck" and self.player.colliderect(obj["rect"]):
                self.objects.remove(obj)

        self.app = QApplication.instance()
        if not self.app:
            self.app = QApplication([])

    def load_player_skin(self):
        #first try using the skin name passed as parameter
        if self.skin_name:
            skin_path = os.path.join("assets/skins", f"{self.skin_name.lower()}.png")
            if os.path.exists(skin_path):
                try:
                    self.player_image = pygame.image.load(skin_path)
                    return
                except pygame.error:
                    print(f"Couldn't load skin image: {skin_path}")

        #then try loading from the preference file
        try:
            if os.path.exists("skin_preference.json"):
                with open("skin_preference.json", "r") as file:
                    data = json.load(file)
                    skin = data.get("skin", None)
                    if skin and "name" in skin:
                        skin_name = skin["name"].lower()
                        skin_path = os.path.join("assets/skins", f"{skin_name}.png")
                        if os.path.exists(skin_path):
                            self.player_image = pygame.image.load(skin_path)
                            self.skin_name = skin_name
                            return
        except Exception as e:
            print(f"Error loading skin preference: {e}")

        #default to frog skin or plain rectangle if that fails
        try:
            self.player_image = pygame.image.load("assets/skins/frog.png")
            self.skin_name = "frog"
        except pygame.error:
            print("Couldn't load default skin. Using colored rectangle.")
            self.player_image = None

    def load_level_data(self, filepath):
        #load and parse each line of the file to get terrain patterns
        try:
            with open(filepath, "r") as file:
                level_data = [ast.literal_eval(line.strip()) for line in file]
            return level_data
        except Exception as e:
            print(f"Problem loading level data: {e}")
            return []

    def add_initial_rows(self):
        start_y = self.camera_y
        for i, terrain_list in enumerate(self.next_rows):
            y = start_y + i * self.sizeh
            
            # For rows 0-9, we know they're grass because we set them in __init__
            self.add_new_rows(terrain_list, y)

            # Set player position on the 5th grass row for better visibility
            if i == 5:
                middle_col = len(terrain_list) // 2
                x = middle_col * self.sizew
                self.player.x = x + (self.sizew - self.player_size) // 2
                self.player.y = self.height // 2 - self.player_size // 2
                print(f"Player positioned at: {self.player} on grass row {i}")

    def add_new_rows(self, terrain_list, y):
        cols = int(self.width / self.sizew)

        #calculate elapsed time in seconds - using floating point division
        elapsed_seconds = (pygame.time.get_ticks() - self.game_start_time) / 1000.0

        for col, terrain in enumerate(terrain_list):
            if terrain in self.obstacle_types:
                props = self.obstacle_types[terrain]
                x = col * self.sizew

                #always add the road first if the terrain is a road
                if props['type'] == "road":
                    road_obj = {
                        "rect": pygame.Rect(x, y, self.sizew, self.sizeh),
                        "color": props['color'],
                        "type": "road"
                    }
                    self.objects.append(road_obj)

                    # Debug print to check the timing
                    if col == 0:
                        print(f"Road added at time: {elapsed_seconds:.1f}s")

                    #add a truck only if more than 5 seconds have elapsed
                    if elapsed_seconds > 5.0 and random.random() < 0.2:
                        truck_obj = {
                            "rect": pygame.Rect(x, y, self.sizew * 2, self.sizeh),
                            "color": self.red,
                            "type": "truck"
                        }
                        print(f"Created truck at {truck_obj['rect']} at elapsed time {elapsed_seconds:.1f}s")
                        self.objects.append(truck_obj)
                else:
                    #add other terrain types (e.g., grass, water, etc.)
                    obj = {
                        "rect": pygame.Rect(x, y, self.sizew, self.sizeh),
                        "color": props['color'],
                        "type": props['type']
                    }
                    self.objects.append(obj)

    def handle_events(self):
        keys = pygame.key.get_pressed()
        moved = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        #check for collisions with objects - with camera offsets applied
        for obj in self.objects:
            #create adjusted rectangle for collision detection
            adjusted_obj_rect = obj["rect"].copy()
            #adjust the Y coordinate for camera position (X remains absolute)
            adjusted_obj_rect.y -= self.camera_y
            
            #check for truck collisions
            if obj["type"] == "truck" and self.player.colliderect(adjusted_obj_rect):
                print(f"Collision detected! Player at {self.player}, Truck at {adjusted_obj_rect}")
                self.game_over = True
                self.game_over_message = f"Game Over, {self.username}! You were hit by a truck!"
                return False
                
            #check for water collisions
            elif obj["type"] == "water" and self.player.colliderect(adjusted_obj_rect):
                print(f"Water collision detected! Player at {self.player}, Water at {adjusted_obj_rect}")
                self.game_over = True
                self.game_over_message = f"Game Over, {self.username}! You fell into the water!"
                return False

        #add a boost mechanism
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            boost = 5
        else:
            boost = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.x -= self.player_speed + boost
            moved = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.x += self.player_speed + boost
            moved = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player.y -= self.player_speed + boost
            moved = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player.y += self.player_speed + boost
            moved = True

        #prevent the player from moving out of bounds
        if self.player.left < 0:
            self.player.left = 0
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.top < 0:
            self.player.top = 0

        #end the game if the player falls behind the screen
        if self.player.bottom >= self.height:
            self.game_over = True
            self.game_over_message = f"Game Over, {self.username}! Too slow - keep up with the screen!"
            return False

        return True

    def update_camera(self):
        try:
            previous_camera_y = self.camera_y
            self.camera_y += self.camera_speed_y

            camera_change = self.camera_y - previous_camera_y
            self.player.y -= camera_change

            #update truck positions and wrap them around
            for obj in self.objects:
                if obj["type"] == "truck":
                    obj["rect"].x += 5
                    if obj["rect"].left > self.width:
                        obj["rect"].right = 0

            #add new rows if needed
            if len(self.objects) == 0 or self.objects[-1]["rect"].top > self.camera_y:
                top_y = self.camera_y - self.sizeh
                
                # Always include at least 3 grass rows at the beginning
                grass_rows_at_start = 3
                if not self.next_rows or len(self.next_rows) < grass_rows_at_start:
                    self.next_rows = []
                    for _ in range(grass_rows_at_start):
                        self.next_rows.append(['g'] * 10)

                for i, terrain_list in enumerate(self.next_rows):
                    y = top_y - (i * self.sizeh)
                    # For the first 3 rows, always force grass
                    if i < grass_rows_at_start:
                        terrain_list = ['g'] * 10
                    self.add_new_rows(terrain_list, y)

                #replenish next_rows when we're running low
                if hasattr(self, 'level_data') and self.level_data:
                    # Always include 3 grass rows at the beginning for safety
                    self.next_rows = []
                    for _ in range(3):
                        self.next_rows.append(['g'] * 10)  
                    
                    # Add the rest from level data
                    for i in range(5):  
                        if i < len(self.level_data):
                            self.next_rows.append(self.level_data[i])
                    
                    self.level_data = self.level_data[5:] if len(self.level_data) > 5 else []
                else:
                    file_path = "random_generations.txt"
                    if os.path.exists(file_path):
                        self.level_data = self.load_level_data(file_path)
                        random.shuffle(self.level_data)
                        
                        # Always include 3 grass rows at the beginning
                        self.next_rows = []
                        for _ in range(3):
                            self.next_rows.append(['g'] * 10)
                        
                        # Add the rest from level data
                        for i in range(5):
                            if i < len(self.level_data):
                                self.next_rows.append(self.level_data[i])
                                
                        self.level_data = self.level_data[5:] if len(self.level_data) > 5 else []
                    else:
                        print("Oops! Lost the level data file during gameplay!")
                        self.game_over = True
                        self.game_over_message = f"Game Over, {self.username}! Level data went missing."

            #keep object count under control
            max_objects = 1000
            if len(self.objects) > max_objects:
                self.objects = self.objects[-max_objects:]

            #remove objects that are out of view
            self.objects = [obj for obj in self.objects if obj["rect"].top < self.camera_y + self.height]

        except Exception as e:
            print(f"Camera update error: {e}")

    def draw(self):
        try:
            self.screen.fill(self.white)

            #debug variables to count objects
            trucks_drawn = 0
            water_tiles = 0
            grass_tiles = 0

            for obj in self.objects:
                rect = obj["rect"].move(-self.camera_x, -self.camera_y)

                if obj["type"] == "log" and self.log_image:
                    self.screen.blit(self.log_image, rect)
                elif obj["type"] == "truck":
                    trucks_drawn += 1
                    if self.truck_image:
                        self.screen.blit(self.truck_image, rect)
                    else:
                        pygame.draw.rect(self.screen, self.red, rect)
                    
                    #draw a border around the truck for debug visibility
                    pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
                else:
                    pygame.draw.rect(self.screen, obj["color"], rect)
                    if obj["type"] == "water":
                        water_tiles += 1
                        #add a blue border around water tiles for visibility
                        pygame.draw.rect(self.screen, (0, 0, 128), rect, 1)
                    elif obj["type"] == "grass":
                        grass_tiles += 1
                        #add a dark green border around grass tiles for visibility
                        pygame.draw.rect(self.screen, (0, 100, 0), rect, 1)

                #draw road markings on road tiles
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

            #draw the player character
            if self.player_image:
                scaled_image = pygame.transform.scale(self.player_image, (self.player_size, self.player_size))
                self.screen.blit(scaled_image, self.player)
            else:
                pygame.draw.rect(self.screen, self.black, self.player)
                
            #draw a border around the player for debug visibility
            pygame.draw.rect(self.screen, (255, 0, 0), self.player, 2)

            #show debug info on screen
            font = pygame.font.Font(None, 24)
            score = abs(int(self.camera_y))
            elapsed_seconds = (pygame.time.get_ticks() - self.game_start_time) / 1000.0
            debug_text = font.render(f"Score: {score} | Camera Y: {self.camera_y} | Trucks: {trucks_drawn} | Water: {water_tiles} | Grass: {grass_tiles} | Time: {elapsed_seconds:.1f}s", True, self.black)
            self.screen.blit(debug_text, (10, 10))

            pygame.display.flip()
        except Exception as e:
            print(f"Drawing error: {e}")

    def run(self):
        running = True
        frame_count = 0
        try:
            while running:
                frame_count += 1
                if frame_count % 300 == 0:
                    print(f"Frame {frame_count}, Camera Y: {self.camera_y}, Objects: {len(self.objects)}")

                running = self.handle_events()
                if running:
                    self.update_camera()
                    self.draw()
                self.clock.tick(30)

        except Exception as e:
            print(f"Game loop error: {e}")

        if self.game_over:
            pygame.quit()
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Game Over")
            msg_box.setText(self.game_over_message)
            msg_box.exec_()
        else:
            pygame.quit()


def main(username="player", skin_name=None):
    #main entry function that creates and runs the game
    try:
        game = ChangingScreen(username=username, skin_name=skin_name)
        game.run()
    except Exception as e:
        print(f"Error: {e}")
        pygame.quit()

#direct execution - run the game when this script is executed
username = "player"
skin_name = None

#check command line arguments
if len(sys.argv) > 1:
    username = sys.argv[1]

if len(sys.argv) > 2:
    skin_name = sys.argv[2]

#run the main function
main(username, skin_name)