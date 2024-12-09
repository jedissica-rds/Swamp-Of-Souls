import pygame
import constants as constant
import time
from levels.HUD import HUD
from constants import WHITE

# Initializing Pygame
pygame.init()

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game Screen
game_screen = pygame.display.set_mode((constant.WIDTH, constant.HEIGHT))  # Changed 'screen' to 'game_screen'
pygame.display.set_caption("Swamp of Souls")

# Background images
bg_images = [pygame.image.load(f'assets/background/BG_{i}.png').convert_alpha() for i in range(2, 6)]
bg_width = bg_images[0].get_width()


class Level:

    def __init__(self, WIDTH, HEIGHT, sanidade_maxima, cor_texto=WHITE):
        self.scroll = 0
        self.opacity = 100

        self.hud = HUD(WIDTH, HEIGHT, sanidade_maxima, cor_texto)

    def atualizar(self):
            # Atualizar atributos do HUD com base no nível
            self.hud.out_of_the_way = self.scroll / 10
            if self.hud.out_of_the_way > 100:
                self.hud.out_of_the_way = 100

            self.hud.errors = int(self.opacity / 20)
            self.hud.sanidade_atual -= 0.1
            if self.hud.sanidade_atual < 0:
                self.hud.sanidade_atual = 0

    def desenhar(self, tela):
            # Desenha a HUD na tela
            self.hud.desenhar_barra_sanidade(tela, 50, 50)
            self.hud.exibir_texto_sanidade(tela, 50, 90)
            self.hud.exibir_progresso(tela, 180, 30)
            self.hud.exibir_erros(tela, 180, 70)

    def draw_background(self, static_image):
        game_screen.blit(static_image, (0, 0))

        for x in range(6):
            speed = 1
            for l in bg_images:
                game_screen.blit(l, ((x * bg_width) - self.scroll * speed, 0))
                speed += 0.6

    def darken_screen(self):
        control = 5
        dark_overlay = pygame.Surface((constant.WIDTH, constant.HEIGHT)).convert()
        dark_overlay.set_alpha(self.opacity)
        dark_overlay.fill(constant.BLACK)
        game_screen.blit(dark_overlay, (0, 0))

    def show_game_over_screen(self, game_over_background):
        # Exibe a tela de Game Over
        game_screen.blit(game_over_background, (0, 0))
        pygame.display.update()
        time.sleep(3)  # Pausa por 3 segundos

    def create_letter_row(self, text):
        with open('assets/font/LetterRow', 'r') as file:
            letter_row = [line.rstrip('\n').replace("'", "") for line in file]
        return letter_row
