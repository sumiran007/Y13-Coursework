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
        
        #Check if the skins folder exists
        if os.path.exists(skins_dir):
            #Grab all image files
            skin_files = [f for f in os.listdir(skins_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
            
            # Find the frog.png to make it the default (first in the list)
            frog_skin_index = -1
            for i, filename in enumerate(skin_files):
                if filename.lower() == "frog.png":
                    frog_skin_index = i
                    break
            
            # If frog.png exists, move it to the front of the list
            if frog_skin_index != -1:
                skin_files.insert(0, skin_files.pop(frog_skin_index))
            
            # Load all skin images
            for filename in skin_files:
                try:
                    image_path = os.path.join(skins_dir, filename)
                    image = pygame.image.load(image_path)
                    #Get skin name from filename
                    skin_name = os.path.splitext(filename)[0].capitalize()
                    
                    skin = {
                        "name": skin_name,
                        "image": image,
                        "color": None  #No color for image skins
                    }
                    skins.append(skin)
                except pygame.error:
                    print(f"Couldn't load skin image: {filename}")
        
        # If no skins were loaded, create a basic colored square as a fallback
        if not skins:
            fallback_surface = pygame.Surface((64, 64))
            fallback_surface.fill((34, 139, 34))  # Green color
            skins.append({
                "name": "Default",
                "image": fallback_surface,
                "color": None
            })
            print("Warning: No skin images found in assets/skins directory. Using fallback skin.")
        
        return skins
    
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