import pygame
import os
from PyQt5.QtWidgets import QApplication, QMessageBox

class SkinSelector:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.width, self.height = width, height  #window size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Skin Selection")
        self.clock = pygame.time.Clock()
        
        #Colors
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gray = (200, 200, 200)
        self.light_gray = (230, 230, 230)
        self.blue = (0, 0, 255)
        
        #Button stuff
        self.button_width = 100
        self.button_height = 50
        self.button_color = self.gray
        self.button_hover_color = self.light_gray
        self.button_text_color = self.black
        
        #Load all the skins
        self.skins = self.load_skins()
        self.current_skin_index = 0
        
        #Make the buttons
        self.left_button = pygame.Rect(
            50, 
            self.height // 2, 
            self.button_width, 
            self.button_height
        )
        
        self.right_button = pygame.Rect(
            self.width - 50 - self.button_width, 
            self.height // 2, 
            self.button_width, 
            self.button_height
        )
        
        self.select_button = pygame.Rect(
            self.width // 2 - self.button_width // 2,
            self.height - 100,
            self.button_width,
            self.button_height
        )
        
        #Will hold chosen skin
        self.selected_skin = None
        
        #Setup QApplication for message boxes
        self.app = QApplication.instance()
        if not self.app:
            self.app = QApplication([])
    
    def load_skins(self):
        #Get all skins from assets/skins folder
        skins = []
        skins_dir = "assets/skins"
        
        #Make a default frog skin
        default_skin = {
            "name": "Frog",
            "image": self.create_frog_skin(),  #Make a simple frog programmatically
            "color": None
        }
        skins.append(default_skin)
        
        #Check if the skins folder exists
        if os.path.exists(skins_dir):
            #Grab all image files
            for filename in os.listdir(skins_dir):
                if filename.endswith(('.png', '.jpg', '.jpeg')):
                    try:
                        image_path = os.path.join(skins_dir, filename)
                        image = pygame.image.load(image_path)
                        #Get skin name from filename
                        skin_name = os.path.splitext(filename)[0]
                        
                        skin = {
                            "name": skin_name,
                            "image": image,
                            "color": None  #No color for image skins
                        }
                        skins.append(skin)
                    except pygame.error:
                        print(f"Couldn't load skin image: {filename}")
        
        return skins

    def create_frog_skin(self):
        #Draw a simple frog
        size = 64
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        #Frog body (green oval)
        frog_green = (34, 139, 34)  #Forest green
        pygame.draw.ellipse(surface, frog_green, (0, 10, size, size-20))
        
        #Frog eyes (white circles with black pupils)
        eye_size = size // 6
        pygame.draw.circle(surface, (255, 255, 255), (size//3, size//3), eye_size)
        pygame.draw.circle(surface, (255, 255, 255), (2*size//3, size//3), eye_size)
        
        #Pupils
        pupil_size = eye_size // 2
        pygame.draw.circle(surface, (0, 0, 0), (size//3, size//3), pupil_size)
        pygame.draw.circle(surface, (0, 0, 0), (2*size//3, size//3), pupil_size)
        
        #Frog legs
        leg_color = (26, 120, 26)  #Slightly darker green
        #Back legs
        pygame.draw.ellipse(surface, leg_color, (5, size-20, size//4, size//3))
        pygame.draw.ellipse(surface, leg_color, (size-size//4-5, size-20, size//4, size//3))
        
        #Front legs
        pygame.draw.ellipse(surface, leg_color, (size//5, size//2, size//5, size//3))
        pygame.draw.ellipse(surface, leg_color, (3*size//5, size//2, size//5, size//3))
        
        return surface
    
    def draw_button(self, button, text):
        #Draw a button with text
        mouse_pos = pygame.mouse.get_pos()
        
        #Check if mouse is hovering over button
        if button.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.button_hover_color, button)
        else:
            pygame.draw.rect(self.screen, self.button_color, button)
        
        #Draw border
        pygame.draw.rect(self.screen, self.black, button, 2)
        
        #Draw the text
        font = pygame.font.Font(None, 24)
        text_surface = font.render(text, True, self.button_text_color)
        text_rect = text_surface.get_rect(center=button.center)
        self.screen.blit(text_surface, text_rect)
    
    def draw_skin_preview(self):
        #Show the current skin in the middle
        skin = self.skins[self.current_skin_index]
        
        #Show skin name
        font = pygame.font.Font(None, 36)
        name_text = font.render(skin["name"], True, self.black)
        name_rect = name_text.get_rect(center=(self.width // 2, 50))
        self.screen.blit(name_text, name_rect)
        
        #Make preview box
        preview_size = 100
        preview_rect = pygame.Rect(
            self.width // 2 - preview_size // 2,
            self.height // 2 - preview_size // 2,
            preview_size,
            preview_size
        )
        
        #Draw the skin
        if skin["image"]:
            #Scale image to fit preview box
            scaled_image = pygame.transform.scale(skin["image"], (preview_size, preview_size))
            self.screen.blit(scaled_image, preview_rect)
        else:
            #Draw colored rectangle if no image
            pygame.draw.rect(self.screen, skin["color"], preview_rect)
    
    def run(self):
        #Run the skin selector
        running = True
        
        while running:
            self.screen.fill(self.white)
            
            #Draw buttons and skin preview
            self.draw_button(self.left_button, "< Prev")
            self.draw_button(self.right_button, "Next >")
            self.draw_button(self.select_button, "Select")
            self.draw_skin_preview()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    #Left button - previous skin
                    if self.left_button.collidepoint(mouse_pos):
                        self.current_skin_index = (self.current_skin_index - 1) % len(self.skins)
                    
                    #Right button - next skin
                    elif self.right_button.collidepoint(mouse_pos):
                        self.current_skin_index = (self.current_skin_index + 1) % len(self.skins)
                    
                    #Select button - use this skin
                    elif self.select_button.collidepoint(mouse_pos):
                        self.selected_skin = self.skins[self.current_skin_index]
                        running = False
            
            pygame.display.flip()
            self.clock.tick(30)
        
        pygame.quit()
        return self.selected_skin

def select_skin():
    #Quick function to run the skin selector
    selector = SkinSelector()
    return selector.run()

if __name__ == "__main__":
    #Testing the skin selector
    skin = select_skin()
    if skin:
        print(f"You picked: {skin['name']}")
    else:
        print("You didn't pick a skin")