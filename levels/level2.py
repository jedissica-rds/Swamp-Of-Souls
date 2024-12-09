import sys

import pygame
import time
from levels import level
import constants as constant
import levels.player as player_mod
from constants import WHITE

# Initializing Pygame
pygame.init()

# Clock
clock = pygame.time.Clock()
FPS = 60

# Defining fonts
last_letter_position = 0
last_letter = 0

# Screen dimensions
game_screen = pygame.display.set_mode((constant.WIDTH, constant.HEIGHT))
pygame.display.set_caption("Swamp of Souls")

# Background and images
bg_images = []
for i in range(2, 6):
    bg_image = pygame.image.load(f'assets/background/BG_{i}.png').convert_alpha()
    bg_images.append(bg_image)
bg_width = bg_images[0].get_width()

static_bg_image = pygame.image.load(f'assets/background/BG_1.png').convert_alpha()

# Sounds
background_sound = pygame.mixer.Sound('assets/sounds-effects/witch-forest-atmo-24654.mp3')
background_sound.set_volume(0.5)
background_sound.play()

game_over_background = pygame.image.load('assets/background/GAMEOVER2.png').convert()


class LevelTwoScreen(level.Level):
    def __init__(self, WIDTH, HEIGHT, max_sanity, cor_texto=WHITE):
        super().__init__(WIDTH, HEIGHT, max_sanity, cor_texto=WHITE)
        self.running = True
        self.tree_l_x = 0
        self.tree_r_x = constant.WIDTH - 450
        self.shadow_alpha = 255
        self.player = player_mod.Player(constant.WIDTH / 2 - 350, 370, "Right")
        self.text_alpha = 255
        self.animation_duration = 120
        self.transparency = 255
        self.transparency_value = 1
        self.letter_color = constant.OFF_WHITE
        self.error_time = 0
        self.error_color_duration = 0.4
        self.last_letter = ''
        self.last_letter_position = 0
        self.letter_row = self.create_letter_row()
        self.current_letter_index = 0
        self.time = pygame.time
        self.moving_sprites = pygame.sprite.Group()
        self.moving_sprites.add(self.player)
        self.key_images = {
            letter.upper(): pygame.image.load(
                f'./assets/keys/key_{letter.upper().replace(" ", "")}.png').convert_alpha()
            for letter in self.letter_row

        }
        self.image_letter = pygame.transform.scale(self.key_images[self.letter_row[0].upper()], (100, 100))

    def lower_opacity(self):
        if self.transparency >= 0:
            self.transparency -= int(self.transparency_value)

    def create_letter_row(self):
        with open('assets/font/LetterRowLevel02.txt', 'r') as file:
            return [line.rstrip('\n').replace("'", "") for line in file]

    def draw_letters(self):
        x, y = (constant.WIDTH / 2 - 200), 470
        shadow_offset = 2
        last_paw = 0
        for index, letter in enumerate(self.letter_row):
            if index == self.current_letter_index and self.error_time and time.time() - self.error_time < self.error_color_duration:
                self.letter_color = constant.RED
            else:
                self.letter_color = constant.WHITE

            shadow_text = constant.font.render(letter, True, (50, 50, 50))
            shadow_text.set_alpha(self.transparency)
            game_screen.blit(shadow_text, (x + shadow_offset, y + shadow_offset))

            text = constant.font.render(letter, True, self.letter_color)
            text.set_alpha(self.transparency)
            image = pygame.transform.scale(pygame.image.load(
                'assets/objects/Animal Footstep.png').convert_alpha(), (50, 50))
            image.set_alpha(self.transparency)
            game_screen.blit(text, (x, y))

            if last_paw == 0:
                game_screen.blit(image, (x, y + 140))
                last_paw = 1
            elif last_paw == 1:
                game_screen.blit(image, (x, y + 120))
                last_paw = 0
            x += text.get_width() + 50

            if index == len(self.letter_row) - 1:
                self.last_letter = self.letter_row[-1]
                self.last_letter_position = x

    def reset(self):
        self.running = True
        self.tree_l_x = 0
        self.tree_r_x = constant.WIDTH - 450
        self.shadow_alpha = 255
        self.player = player_mod.Player(constant.WIDTH / 2 - 350, 370, "Right")
        self.text_alpha = 255
        self.animation_duration = 120
        self.transparency = 255
        self.transparency_value = 1
        self.letter_color = constant.OFF_WHITE
        self.error_time = 0
        self.error_color_duration = 0.4
        self.last_letter = ''
        self.last_letter_position = 0
        self.letter_row = self.create_letter_row()
        self.current_letter_index = 0
        self.time = pygame.time
        self.moving_sprites = pygame.sprite.Group()
        self.moving_sprites.add(self.player)
        self.key_images = {
            letter.upper(): pygame.image.load(
                f'./assets/keys/key_{letter.upper().replace(" ", "")}.png').convert_alpha()
            for letter in self.letter_row

        }
        self.image_letter = pygame.transform.scale(self.key_images[self.letter_row[0].upper()], (100, 100))

    def run(self):
        self.running = True

        while self.running:
            game_screen.fill(constant.WHITE)

            clock.tick(FPS)
            self.draw_background(static_bg_image)
            self.moving_sprites.draw(game_screen)

            # level_text = constant.normal_font.render(f"Level 3", True, constant.WHITE)
            # game_screen.blit(level_text, (600, 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.unicode.upper() == self.letter_row[0].upper():
                        constant.click_sound.play()
                        self.letter_row.pop(0)
                        self.player.animate()
                        self.transparency = 255

                        if len(self.letter_row) > 0:
                            self.image_letter = pygame.transform.scale(self.key_images[self.letter_row[0].upper()], (100, 100))
                    else:
                        self.error_time = time.time()
                        self.transparency = max(0, self.transparency - 40)

            self.hud.update_timer()
            self.hud.text_sanity(game_screen, 50, 50)

            keys = pygame.key.get_pressed()
            if not any(keys) and not self.player.isAnimating:
                self.player.stopAnimating()

            game_screen.blit(self.image_letter, (30, 30))

            if self.player.isAnimating:
                self.moving_sprites.update(0.4)
                self.scroll += 6

            if abs(self.scroll) > bg_width:
                self.scroll = 0
            elif abs(self.scroll) < 0:
                self.scroll = bg_width

            # self.moving_sprites.draw(game_screen)
            self.lower_opacity()
            self.draw_letters()

            if self.transparency <= 0:
                self.show_game_over_screen(game_over_background)
                self.reset()
            elif len(self.letter_row) <= 0:
                self.running = False
            # self.darken_screen()
            pygame.display.update()
            clock.tick(FPS)
