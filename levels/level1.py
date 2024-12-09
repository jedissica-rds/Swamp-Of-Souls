import pygame
import levels.player as player_mod
from constants import WHITE
from intervals.interval1 import Firefly
import constants as constant
from levels import level
from intervals.interval4 import screen

# Initializing Pygame
pygame.init()

# Clock
clock = pygame.time.Clock()
FPS = 60

# Screen
game_screen = pygame.display.set_mode((constant.WIDTH, constant.HEIGHT))  # Changed 'screen' to 'game_screen'
pygame.display.set_caption("Swamp of Souls")

# Background images
static_background = pygame.image.load(f'assets/background/BG_1.png')
bg_images = [pygame.image.load(f'assets/background/BG_{i}.png').convert_alpha() for i in range(2, 6)]
bg_width = bg_images[0].get_width()

# Players sounds
background_sound = pygame.mixer.Sound('assets/sounds-effects/Alone at Twilight 5.wav')
background_sound.set_volume(0.5)  # Set volume to 50%
background_sound.play()

# Jar
jar = pygame.transform.scale(pygame.image.load('assets/objects/jar.png').convert_alpha(), (60, 60))
jar_positions = [constant.WIDTH - 60, constant.HEIGHT - 150]

class LevelOneScreen(level.Level):
    def __init__(self, WIDTH, HEIGHT, max_sanity, cor_texto=WHITE):
        super().__init__(WIDTH, HEIGHT, max_sanity, cor_texto=WHITE)
        self.moving_sprites = pygame.sprite.Group()
        self.player = player_mod.Player(40, 370, "Right")
        self.moving_sprites.add(self.player)
        self.player_position = [600, 370]
        self.fireflies = pygame.sprite.Group()

        # Creating fireflies
        for _ in range(10):
            firefly = Firefly()
            self.fireflies.add(firefly)

    def atualizar(self):
        # Chama a lógica de atualização da classe mãe
        super().atualizar()

    def run(self):
        running = True

        # Font for displaying letters
        font = constant.x_small_font
        # Key pressed tracker
        key_pressed = None

        while running:
            game_screen.fill(constant.WHITE)
            clock.tick(FPS)

            # Drawing and updating sprites
            self.draw_background(static_background)
            game_screen.blit(self.player.image, (self.player_position[0], self.player_position[1]))
            self.player.grab_jar()

            # Event handling
            key_pressed = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        constant.click_sound.play()
                        key_pressed = "F"
                    elif event.key == pygame.K_j:
                        constant.click_sound.play()
                        key_pressed = "J"

            self.hud.update_timer()
            self.hud.text_sanity(screen, 50, 50)

            # Update fireflies and check for "catch" interaction
            caught = False
            for firefly in self.fireflies:
                key_text = font.render(firefly.catch_key, True, constant.YELLOW)
                game_screen.blit(key_text, (firefly.rect.x, firefly.rect.y - 20))

                # Check collision and correct key
                if not caught and key_pressed == firefly.catch_key:
                    # Firefly caught
                    print(f"Firefly with key '{firefly.catch_key}' caught at ({firefly.rect.x}, {firefly.rect.y})!")
                    self.fireflies.remove(firefly)
                    self.opacity = max(0, self.opacity - 20)
                    caught = True  # Set flag to True to exit loop after catching one firefly
                    self.player.catch_firefly()
                    break  # Stop after catching one firefly

            if len(self.fireflies) == 0:
                # Fade-out effect
                self.opacity =  min(255, self.opacity + 5)
                if self.opacity == 255:
                    running = False

            if abs(self.scroll) > bg_width:
                self.scroll = 0
            elif abs(self.scroll) < 0:
                self.scroll = bg_width

            self.moving_sprites.update(0.25)
            self.darken_screen()
            # Update fireflies
            self.fireflies.update()

            # Draw fireflies on screen
            self.fireflies.draw(game_screen)

            pygame.display.update()
