import random
import sys

import pygame
import time
import math
import player as player_mod

# Initializing Pygame
pygame.init()

# Clock
clock = pygame.time.Clock()
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (185, 185, 185)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
FIREFLY_COLOR = (239,204,0)

# Defining fonts
small_font = pygame.font.Font("assets/IMFellEnglish-Regular.ttf", 24)
x_small_font = pygame.font.Font("assets/IMFellEnglish-Regular.ttf", 16)

# Screen dimensions
WIDTH, HEIGHT = 1320, 680
game_screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Changed 'screen' to 'game_screen'
pygame.display.set_caption("Swamp of Souls")

# Background images
bg_images = [pygame.image.load(f'assets/background/BG_{i}.png').convert_alpha() for i in range(2, 6)]
bg_width = bg_images[0].get_width()

# Players sounds
background_sound = pygame.mixer.Sound('assets/sounds-effects/Alone at Twilight 5.wav')
click_sound = pygame.mixer.Sound('assets/click-keyboard.mp3')
background_sound.set_volume(0.5)  # Set volume to 50%
background_sound.play()

# Jar
jar = pygame.transform.scale(pygame.image.load('assets/objects/jar.png').convert_alpha(), (60, 60))
jar_positions = [WIDTH - 60, HEIGHT - 150]


class Firefly(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Create a larger surface with alpha transparency for the firefly
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)  # Increased size to 50x50

        self.catch_key = random.choice(["F", "J"])
        # Draw a larger firefly circle in the center of the surface
        pygame.draw.circle(self.image, FIREFLY_COLOR, (25, 25), 10)
        self.rect = self.image.get_rect()

        # Random initial position
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(0, HEIGHT)

        # Initialize transparency and fading speed
        self.alpha = random.randint(50, 255)  # Set initial transparency
        self.fade_speed = random.uniform(1, 3)  # Set random fade speed
        self.vx = random.uniform(-1, 1)  # Horizontal speed
        self.vy = random.uniform(-1, 1)  # Vertical speed


    def update(self):
        # Movement (existing logic)
        self.rect.x += self.vx
        self.rect.y += self.vy

        # Boundary check to bounce off edges
        if self.rect.x < 0 or self.rect.x > WIDTH - self.rect.width:
            self.vx = -self.vx
        if self.rect.y < 0 or self.rect.y > HEIGHT - self.rect.height:
            self.vy = -self.vy

        # Adjust alpha for pulsing effect
        self.alpha += self.fade_speed
        if self.alpha >= 255:
            self.alpha = 255
            self.fade_speed *= -1  # Reverse direction to start fading out
        elif self.alpha <= 50:
            self.alpha = 50
            self.fade_speed *= -1  # Reverse direction to start fading in

        # Apply updated alpha to image
        self.image.set_alpha(self.alpha)

class IntervalScreen:
    def __init__(self):
        self.scroll = 0
        self.moving_sprites = pygame.sprite.Group()
        self.player = player_mod.Player(40, 370, "Right")
        self.moving_sprites.add(self.player)
        self.player_position = [40, 370]
        self.fireflies = pygame.sprite.Group()

        # Creating fireflies
        for _ in range(15):
            firefly = Firefly()
            self.fireflies.add(firefly)


    def draw_background(self):
        static_bg_image = pygame.image.load(f'assets/background/BG_1.png').convert_alpha()
        game_screen.blit(static_bg_image, (0, 0))

        for x in range(6):
            speed = 1
            for l in bg_images:
                game_screen.blit(l, ((x * bg_width) - self.scroll * speed, 0))
                speed += 0.6

    def darken_screen(self, opacity):
        dark_overlay = pygame.Surface((WIDTH, HEIGHT))
        dark_overlay.set_alpha(opacity)
        dark_overlay.fill(BLACK)
        game_screen.blit(dark_overlay, (0, 0))

    def run(self):
        running = True

        while running:
            game_screen.fill(WHITE)
            clock.tick(FPS)

            self.draw_background()
            game_screen.blit(self.player.image, (self.player_position[0], self.player_position[1]))

            # Check events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.unicode.upper() == 'E' and abs((self.player_position[0] + 36) - jar_positions[0]) < 70:
                        click_sound.play()
                     # Enter level 1 phase
                        running = False
                        # print("Player grabbed the glass")
                        # self.player.grab_jar()  # Change sprite to holding jar

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                self.player.orientation = 'Right'
                if self.player_position[0] < WIDTH - 300:
                    self.player_position[0] += 4
                else:
                    self.scroll += 2
                    jar_positions[0] -= 4
                self.player.animate()
            elif keys[pygame.K_LEFT]:
                self.player.orientation = "Left"

                if self.player_position[0] > 40:
                    self.player_position[0] -= 4
                    if self.scroll > 0:
                        self.scroll -= 2
                        jar_positions[0] += 4
                self.player.animate()
            else:
                self.player.stopAnimating()

            if abs(self.scroll) > bg_width:
                self.scroll = 0
            elif abs(self.scroll) < 0:
                self.scroll = bg_width

            self.moving_sprites.update(0.25)
            self.darken_screen(200)

            # Update fireflies
            self.fireflies.update()

            # Draw fireflies on screen
            self.fireflies.draw(game_screen)

            # Draw jar
            game_screen.blit(jar, (jar_positions[0], jar_positions[1]))

            # Interaction hint
            if abs((self.player_position[0] + 36) - jar_positions[0]) < 70:
                press_e_text = x_small_font.render(f'Pressione E para pegar a jarra', True, WHITE)
                game_screen.blit(press_e_text, (jar_positions[0] + 5, jar_positions[1] - 60))

            # Draw the tip
            text = small_font.render(f'Aqui é muito escuro...Como posso iluminar meu caminho?', True, WHITE)
            game_screen.blit(text, (50, HEIGHT - 60))

            pygame.display.update()
