import pygame
import ast  # For safely parsing the lists from the file
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox

class ChangingScreen:
    def __init__(self, width=800, height=600, sizew=50, sizeh=50, spacing=0, username="player"):  # Set spacing to 0
        pygame.init()
        self.username = username
        self.start_y = 0
        self.width, self.height = width, height
        self.sizew, self.sizeh = sizew, sizeh
        self.spacing = spacing  # No spacing between squares
        self.camera_x, self.camera_y = 0, 0
        self.camera_speed_x, self.camera_speed_y = 0, -5  # Camera moves up
        self.objects = []
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.brown = (139, 69, 19)
        self.black = (0, 0, 0)
        self.grey = (128, 128, 128)
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Frogger Game")
        self.clock = pygame.time.Clock()
        self.level_data = self.load_level_data("random_generations.txt")  # Load obstacle data
        self.current_level = 0  # Start with the first level
        
        # Add game over flag to fix display Surface quit error
        self.game_over = False
        self.game_over_message = ""

        # Adjust square size to fill the screen
        self.sizew = self.width // 10  # Divide the screen width by 10 columns
        self.sizeh = self.height // 10  # Divide the screen height by 10 rows

        # Create player sprite in the middle of the screen
        self.player_size = self.sizew // 2  # Make player smaller than obstacles
        self.player = pygame.Rect(
            self.width // 2 - self.player_size // 2,  # Center horizontally
            self.height // 2 - self.player_size // 2,  # Center vertically
            self.player_size, 
            self.player_size
        )
        
        self.player_speed = 5  # Player movement speed
        self.gravity = 1  # How fast player falls down

        self.add_squares(self.level_data[self.current_level], start_y=self.camera_y)  # Add initial obstacles
        
        # Initialize PyQt for message boxes
        self.app = QApplication.instance()
        if not self.app:
            self.app = QApplication([])

    def load_level_data(self, filepath):
        # Read and parse the file
        with open(filepath, "r") as file:
            level_data = [ast.literal_eval(line.strip()) for line in file]
        return level_data

    def add_squares(self, level_data, start_y=0):
        cols = int(self.width / self.sizew)  # Calculate the number of columns
        for i, symbol in enumerate(level_data):
            x = (i % cols) * self.sizew  # Calculate x position
            y = start_y + (i // cols) * self.sizeh  # Calculate y position

            # Map symbols to colors or obstacle types
            if symbol == 'g':  # Grass
                color = self.green
            elif symbol == 'r':  # road
                color = self.grey
            elif symbol == 'l':  # Log
                color = self.brown
            elif symbol == 'w':  # Water
                color = self.blue
            elif symbol == 's':  # Stone
                color = self.black
            else:
                continue  # Skip unknown symbols

            # Add the obstacle as a rectangle with the corresponding color
            self.objects.append({"rect": pygame.Rect(x, y, self.sizew, self.sizeh), "color": color})

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        
        # Handle player movement with keyboard
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
            
        # Apply "gravity" - player slowly falls down
        self.player.y += self.gravity
            
        # Check if player hits edge of screen
        if (self.player.left <= 0 or 
            self.player.right >= self.width or 
            self.player.top <= 0):
            
            # Set game over flag instead of quitting pygame immediately
            self.game_over = True
            self.game_over_message = f"Game Over, {self.username}! You hit the edge of the screen."
            return False
            
        # Special case for bottom edge - "treadmill" effect
        if self.player.bottom >= self.height:
            # Set game over flag instead of quitting pygame immediately
            self.game_over = True
            self.game_over_message = f"Game Over, {self.username}! You couldn't keep up with the treadmill!"
            return False
            
        return True

    def update_camera(self):
        # Move the camera upward
        self.camera_y += self.camera_speed_y

        # Generate new obstacles continuously as the camera moves
        while len(self.objects) == 0 or self.objects[-1]["rect"].top > self.camera_y:
            # Add new obstacles ABOVE the current view
            self.add_squares(self.level_data[self.current_level], start_y=self.camera_y - self.sizeh)

        # Remove obstacles that are completely below the window
        self.objects = [obj for obj in self.objects if obj["rect"].top < self.camera_y + self.height]

        # Cycle through levels if needed
        if self.camera_y < -self.height * (self.current_level + 1):
            self.current_level = (self.current_level + 1) % len(self.level_data)

    def draw(self):
        self.screen.fill(self.white)
        
        # Draw obstacles - adjust position by camera offset
        for obj in self.objects:
            pygame.draw.rect(self.screen, obj["color"], obj["rect"].move(-self.camera_x, -self.camera_y))
        
        # Draw player at fixed position (not affected by camera)
        pygame.draw.rect(self.screen, self.black, self.player)
        
        # Debug info - show player position and camera position
        font = pygame.font.Font(None, 24)
        score = abs(int(self.camera_y))
        debug_text = font.render(f"Score: {score} | Camera Y: {self.camera_y}", True, self.black)
        self.screen.blit(debug_text, (10, 10))
        
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            if running:  # Only update and draw if game is still running
                self.update_camera()
                self.draw()
            self.clock.tick(30)
            
        # Handle game over outside the main loop
        if self.game_over:
            pygame.quit()  # Now it's safe to quit pygame
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
    # If run directly, use command line arguments for username if provided
    username = "player"
    if len(sys.argv) > 1:
        username = sys.argv[1]
    main(username)