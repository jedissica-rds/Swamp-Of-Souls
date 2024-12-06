import time

import pygame
import player as player_mod

pygame.init()

# Clock
clock = pygame.time.Clock()
FPS = 60
WIDTH, HEIGHT = 1320, 680
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Swamp of Souls")

frame1 = pygame.transform.scale(pygame.image.load('assets/backgrounds/FASE 4.png').convert_alpha(),(1320,680))
frame2 = pygame.transform.scale(pygame.image.load('assets/backgrounds/FASE 4-1.png').convert_alpha(),(1320,680))
frame3 = pygame.transform.scale(pygame.image.load('assets/backgrounds/FASE 4-2.png').convert_alpha(),(1320,680))
frame8 = pygame.transform.scale(pygame.image.load('assets/backgrounds/FASE 4-3.png').convert_alpha(),(1320,680))
frame5 = pygame.transform.scale(pygame.image.load('assets/backgrounds/FASE 4-4.png').convert_alpha(),(1320,680))
frame6 = pygame.transform.scale(pygame.image.load('assets/backgrounds/FASE 4-5.png').convert_alpha(),(1320,680))
frame7 = pygame.transform.scale(pygame.image.load('assets/backgrounds/FASE 4-6.png').convert_alpha(),(1320,680))
frame4 = pygame.transform.scale(pygame.image.load('assets/backgrounds/FASE 4-7.png').convert_alpha(),(1320,680))

class Interval4Screen:
    def __init__(self):

        # Screen background
        self.background_image = pygame.transform.scale(pygame.image.load('assets/backgrounds/BG-6.png'), (1400, 690))

        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (185, 185, 185)
        self.YELLOW = (255, 255, 0)

        # Defining fonts
        self.small_font = pygame.font.Font("assets/IMFellEnglish-Regular.ttf",  24)
        self.x_small_font = pygame.font.Font("assets/IMFellEnglish-Regular.ttf", 16)

        # Sounds
        self.background_sound = pygame.mixer.Sound('assets/Alone at Twilight 5.wav')
        self.click_sound = pygame.mixer.Sound('assets/click-keyboard.mp3')
        self.background_sound.set_volume(0.5)  # Define o volume para 50%
        self.background_sound.play()

        # Player setup
        self.moving_sprites = pygame.sprite.Group()
        self.player = player_mod.Player(40, 370, "Right")
        self.moving_sprites.add(self.player)
        self.player_position = [40, 370]

        # Opacity for fade effect
        self.opacity = 255
        self.fade_speed = 5  # Control the speed of the fade-out effect

    def darken_screen(self):
        if self.opacity > 0:
            dark_overlay = pygame.Surface((WIDTH, HEIGHT))
            dark_overlay.set_alpha(self.opacity)
            dark_overlay.fill(self.BLACK)
            screen.blit(dark_overlay, (0, 0))
            self.opacity -= self.fade_speed  # Reduce opacity to create fade-out effect

    def draw_elements(self):
        # Draw background and player
        screen.fill(self.WHITE)
        screen.blit(self.background_image, (-80, 0))
        screen.blit(self.player.image, (self.player_position[0], self.player_position[1]))

        # Draw the tip
        tip_text = self.small_font.render(f'Estou começando a lembrar, essa ponte...', True, self.WHITE)
        screen.blit(tip_text, (50, HEIGHT - 60))

        if self.player_position[0] > WIDTH - 300:
            press_e_text = self.x_small_font.render(f'Pressione E', True, self.WHITE)
            screen.blit(press_e_text, (WIDTH - 100, HEIGHT - 300))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.unicode.upper() == 'E' and self.player_position[0] > WIDTH - 230:
                    self.click_sound.play()
                    self.show_frames_screen()
                    return False
        return True

    def update_player_position(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.player.orientation = 'Right'
            if self.player_position[0] < WIDTH - 200:
                self.player_position[0] += 3
            self.player.animate()
        elif keys[pygame.K_LEFT]:
            self.player.orientation = "Left"
            if self.player_position[0] > 40:
                self.player_position[0] -= 3
            self.player.animate()
        else:
            self.player.stopAnimating()

    def show_frames_screen(self):
        screen.fill(self.WHITE)
        screen.blit(frame1, (0, 0))
        pygame.display.update()
        time.sleep(2)  # Pausa por 2 segundos
        screen.fill(self.WHITE)
        screen.blit(frame2, (0, 0))
        pygame.display.update()
        time.sleep(2)
        screen.fill(self.WHITE)
        screen.blit(frame3, (0, 0))
        pygame.display.update()
        time.sleep(3)
        screen.fill(self.WHITE)
        screen.blit(frame4, (0, 0))
        pygame.display.update()
        time.sleep(2)  # Pausa por 2 segundos
        screen.fill(self.WHITE)
        screen.blit(frame5, (0, 0))
        pygame.display.update()
        time.sleep(2)
        screen.fill(self.WHITE)
        screen.blit(frame6, (0, 0))
        pygame.display.update()
        time.sleep(3)
        screen.fill(self.WHITE)
        screen.blit(frame7, (0, 0))
        pygame.display.update()
        time.sleep(2)  # Pausa por 2 segundos
        screen.fill(self.WHITE)
        '''
        screen.blit(frame8, (0, 0))
        pygame.display.update()
        time.sleep(2)'''

    def run(self):
        running = True
        while running:
            clock.tick(FPS)
            running = self.handle_events()
            self.update_player_position()
            self.moving_sprites.update(0.20)
            self.draw_elements()
            self.darken_screen()
            pygame.display.update()

        # Stop the background sound after exiting
        self.background_sound.stop()