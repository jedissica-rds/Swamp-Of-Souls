from constants import WHITE, WIDTH, HEIGHT, small_font
import pygame
import time

WIDTH, HEIGHT = WIDTH, HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tela de Teste")

class HUD:
    def __init__(self, WIDTH, HEIGHT, max_sanity, cor_texto=WHITE):
        self.width = WIDTH
        self.height = HEIGHT
        self.max_sanity = 100
        self.sanity = max_sanity
        self.font = small_font
        self.start_time = time.time()
        self.color_text = cor_texto
        self.time_limit = 15

    def update_timer(self):
        current_time = time.time()
        elapsed_time = current_time - self.start_time

        if elapsed_time > self.time_limit:
            self.sanity -= 5
            self.start_time = current_time

    def text_sanity(self, tela, x, y):
        text = self.font.render(f"Sanidade: {int(self.sanity)}%", True, self.color_text)
        tela.blit(text, (150, 100))

hud = HUD(WIDTH, HEIGHT, 100)

