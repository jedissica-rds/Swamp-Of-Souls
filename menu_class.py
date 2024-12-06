# Importing Pygame
import pygame

# Initializing Pygame
pygame.init()

# Clock
clock = pygame.time.Clock()
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

# Screen dimensions
WIDTH, HEIGHT = 1320, 680
game_screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Change from 'screen' to 'game_screen'
pygame.display.set_caption("Swamp of Souls")

# Fonts
title_font = pygame.font.Font("assets/IMFellEnglish-Regular.ttf", 75)
small_font = pygame.font.Font("assets/IMFellEnglish-Regular.ttf", 26)

# Background and images
bg_image = pygame.image.load('assets/backgrounds/bg_menu.png').convert_alpha()
tree_r_image = pygame.transform.scale(pygame.image.load('assets/backgrounds/tree.png').convert_alpha(), (450, 680))
tree_l_image = pygame.transform.flip(tree_r_image, True, False)
shadow_player = pygame.transform.scale(pygame.image.load('assets/objects/shadow.png').convert_alpha(), (39, 69))

# Sounds
background_sound = pygame.mixer.Sound('assets/sounds-effects/Alone at Twilight 5.wav')
click_sound = pygame.mixer.Sound('assets/click-keyboard.mp3')
background_sound.set_volume(0.5)  # Volume 50%
background_sound.play()


class SwampOfSoulsScreen:
    def __init__(self):
        self.tree_l_x = 0
        self.tree_r_x = WIDTH - 450
        self.shadow_alpha = 255
        self.text_alpha = 255
        self.animation_duration = 120
        self.running = True

    @staticmethod
    def set_alpha(surface, alpha):
        temp_surface = surface.copy()
        temp_surface.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
        return temp_surface

    def render_text_with_alpha(self, text, font, color, alpha):
        text_surface = font.render(text, True, color)
        text_surface = self.set_alpha(text_surface, alpha)
        return text_surface

    def animate_closing(self):
        for frame in range(self.animation_duration):
            game_screen.fill(WHITE)  # Use game_screen instead of screen

            # Draw background
            game_screen.blit(bg_image, (0, 0))
            game_screen.blit(tree_r_image, (self.tree_r_x, 0))
            game_screen.blit(tree_l_image, (self.tree_l_x, 0))

            # Draw gray rectangle as ground
            pygame.draw.rect(game_screen, GRAY, (0, HEIGHT - 11, WIDTH, 11))

            # Animate trees
            self.tree_l_x -= 450 / self.animation_duration
            self.tree_r_x += 450 / self.animation_duration

            # Animate shadow fade-out
            self.shadow_alpha -= 255 / self.animation_duration
            if self.shadow_alpha < 0:
                self.shadow_alpha = 0
            faded_shadow = self.set_alpha(shadow_player, int(self.shadow_alpha))
            game_screen.blit(faded_shadow, (675, HEIGHT - 78))

            # Animate text fade-out
            self.text_alpha -= 255 / self.animation_duration
            if self.text_alpha < 0:
                self.text_alpha = 0

            # Render title with fade effect
            title_text1 = self.render_text_with_alpha('Swamp   of', title_font, WHITE, int(self.text_alpha))
            game_screen.blit(title_text1, (490, 129))
            title_text2 = self.render_text_with_alpha('Souls', title_font, WHITE, int(self.text_alpha))
            game_screen.blit(title_text2, (590, 230))

            # Render start text with fade effect
            start_text = self.render_text_with_alpha('press any key to play', small_font, WHITE, int(self.text_alpha))
            game_screen.blit(start_text, (560, HEIGHT - 180))

            pygame.display.update()
            clock.tick(FPS)

    def run(self):
        while self.running:
            game_screen.fill(WHITE)  # Use game_screen instead of screen

            # Draw static elements
            game_screen.blit(bg_image, (0, 0))
            game_screen.blit(tree_r_image, (WIDTH - 450, 0))
            game_screen.blit(tree_l_image, (0, 0))
            game_screen.blit(shadow_player, (675, HEIGHT - 78))
            pygame.draw.rect(game_screen, GRAY, (0, HEIGHT - 11, WIDTH, 11))

            # Draw title
            title_text1 = self.render_text_with_alpha('Swamp   of', title_font, WHITE, 255)
            game_screen.blit(title_text1, (490, 129))
            title_text2 = self.render_text_with_alpha('Souls', title_font, WHITE, 255)
            game_screen.blit(title_text2, (590, 230))

            # Draw start text
            start_text = self.render_text_with_alpha('press any key to play', small_font, WHITE, 255)
            game_screen.blit(start_text, (560, HEIGHT - 180))

            clock.tick(FPS)

            # Check events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    click_sound.play()
                    self.animate_closing()
                    self.running = False

            pygame.display.update()