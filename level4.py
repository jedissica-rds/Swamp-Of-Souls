import pygame
import time
import math
import constants as constant
from constants import *
from HUD import screen
from player import Player
from level import Level

# Inicializando Pygame
pygame.init()

# Configurações principais
clock = pygame.time.Clock()
FPS = 60

# Tela de jogo
game_screen = pygame.display.set_mode((constant.WIDTH, constant.HEIGHT))
pygame.display.set_caption("Swamp of Souls")


# Recursos globais
def load_assets():
    assets = {
        "background": pygame.image.load('assets/background-sky.png').convert(),
        "gameover": pygame.image.load('assets/GAMEOVER4.png').convert(),
        "plank": pygame.transform.scale(pygame.image.load('assets/plank.png').convert_alpha(), (75, 123)),
        "floor": pygame.transform.scale(pygame.image.load('assets/floor.png').convert_alpha(), (320, 250)),
        "moon": pygame.transform.scale(pygame.image.load('assets/objects/moon.png').convert_alpha(), (102, 100)),
        "sounds": {
            "background": pygame.mixer.Sound('assets/witch-forest-atmo-24654.mp3'),
            "bridge": pygame.mixer.Sound('assets/wood-creaking.mp3'),
            "click": pygame.mixer.Sound('assets/click-keyboard.mp3'),
        },
    }
    assets["sounds"]["background"].set_volume(0.5)
    return assets

assets = load_assets()
assets["sounds"]["background"].play()

# Classe Tábua (Plank)
class Plank(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

# Tela de Nível 4
class LevelFourScreen(Level):
    def __init__(self, WIDTH, HEIGHT, max_sanity, cor_texto=WHITE):
        super().__init__(WIDTH, HEIGHT, max_sanity, cor_texto=WHITE)
        self.running = True
        self.bg_w = assets["background"].get_width()
        self.tiles = math.ceil(constant.WIDTH / self.bg_w) + 1
        self.total_planks = 45
        self.crossed_planks = 0
        self.errors = 0
        self.max_errors = 5
        self.start_time = time.time()
        self.time_limit = 3
        self.letter_row = self.create_letter_row('assets/LetterRow.txt')
        self.bridge_stability = 100
        self.error_time = None
        self.error_color_duration = 0.4

        # Grupos de Sprites
        self.planks = pygame.sprite.Group()
        self.player = Player(constant.WIDTH / 2 - 65, 370, "Right")
        self.moving_sprites = pygame.sprite.Group(self.player)

        # Posicionamento das tábuas
        self.plank_positions = [(i * 69, constant.HEIGHT // 2 + 200) for i in range(self.total_planks)]
        for pos in self.plank_positions:
            self.planks.add(Plank(pos[0], pos[1], assets["plank"]))

        self.player_position = [self.plank_positions[0][0], self.plank_positions[0][1] - 200]
        self.scroll = 0  # Controle do movimento do fundo

    def draw_game_state(self, offset_x, stability_y):
        shadow_offset = 2
        player_img = pygame.transform.scale(self.player.image, (112, 200))
        game_screen.blit(player_img,
                         (self.player_position[0] + offset_x - 37, self.player_position[1] + stability_y + 45))
        game_screen.blit(assets["moon"], (605, 53))

        # Texto do nível
        level_text = constant.normal_font.render(f'Level 4', True, constant.WHITE)
        game_screen.blit(level_text, (constant.WIDTH // 2 - 50, 20))

        # Letras restantes
        center_x = constant.WIDTH // 2
        for i, letter in enumerate(self.letter_row):
            letter_color = constant.RED if i == 0 and self.error_time and time.time() - self.error_time < self.error_color_duration else constant.WHITE
            letter_surface = constant.font.render(letter, True, letter_color)
            x_position = center_x + (i * 100)
            shadow_text = constant.font.render(letter, True, (50, 50, 50))
            game_screen.blit(shadow_text, (x_position + shadow_offset, (constant.HEIGHT / 2) - 50 + shadow_offset))
            game_screen.blit(letter_surface, (x_position, constant.HEIGHT // 2 - 50))

        # Informações do jogador
        self.hud.exibir_texto_sanidade(screen, 50, 50)

        # Imagem da próxima letra
        if self.letter_row:
            image_letter = pygame.transform.scale(
                pygame.image.load(
                    f'./assets/keys/key_{self.letter_row[0].upper().replace(" ", "")}.png').convert_alpha(),
                (100, 100))
            game_screen.blit(image_letter, (30, 30))

    def player_jump(self, target_x, target_y, offset_x, stability_y):
        """Animação de pulo com comportamento especial ao final da ponte."""
        start_time = pygame.time.get_ticks()
        duration = 500  # Duração total do pulo em milissegundos
        start_x, start_y = self.player_position
        jump_peak = -100

        while True:
            elapsed_time = pygame.time.get_ticks() - start_time
            t = min(elapsed_time / duration, 1)  # Progresso de 0 a 1

            if self.player_position[0] > constant.WIDTH - 300:
                # Movimento especial perto do final
                self.scroll -= 1

            self.player_position[0] = start_x + (target_x - start_x) * t
            parabola = 4 * jump_peak * t * (1 - t)
            self.player_position[1] = start_y + (target_y - start_y) * t + parabola

            self.render_frame(offset_x, stability_y)
            if t >= 1:
                break
            clock.tick(FPS)

    def draw_bridge(self, offset_x, stability_y):
        for i, pos in enumerate(self.plank_positions):
            x, y = pos[0] + offset_x, pos[1] + stability_y
            game_screen.blit(assets["plank"], (x, y))
        floor_x, floor_y = self.plank_positions[-1][0] + offset_x + 75, self.plank_positions[-1][1]
        game_screen.blit(assets["floor"], (floor_x, floor_y))

    def render_frame(self, offset_x, stability_y):
        game_screen.fill(constant.BLACK)
        for i in range(self.tiles):
            game_screen.blit(assets["background"], (i * self.bg_w + self.scroll, 0))

        self.draw_bridge(offset_x, stability_y)
        self.draw_game_state(offset_x, stability_y)
        pygame.display.flip()

    def run(self):
        offset_x, stability_y = 0, 0

        while self.running:
            self.render_frame(offset_x, stability_y)
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    assets["sounds"]["click"].play()
                    if event.unicode.upper() == self.letter_row[0].upper():
                        self.crossed_planks += 1
                        self.letter_row.pop(0)
                        self.start_time = time.time()
                        if self.crossed_planks < self.total_planks:
                            self.player_jump(
                                self.plank_positions[self.crossed_planks][0] + 12,
                                self.plank_positions[self.crossed_planks][1] - 200 + 45,
                                offset_x, stability_y
                            )
                        if self.player_position[0] > constant.WIDTH - 300:
                            offset_x = constant.WIDTH - 300 - self.player_position[0]
                    else:
                        self.errors += 1
                        self.bridge_stability -= 20
                        stability_y += 30
                        self.error_time = time.time()
                        assets["sounds"]["bridge"].play()

            self.hud.update_timer()
            self.hud.text_sanity(screen, 50, 50)

            # Penalidade de atraso
            if time.time() - self.start_time > self.time_limit:
                self.bridge_stability -= 10
                stability_y += 10
                self.start_time = time.time()
                assets["sounds"]["bridge"].play()

            # Verificar falha
            if self.bridge_stability <= 0 or self.errors >= self.max_errors:
                self.running = False  # Saia ao perder

            # Movimento final ao concluir as tábuas
            if self.crossed_planks >= self.total_planks:
                self.player_position[0] += 5
                if self.player_position[0] > constant.WIDTH:
                    self.running = False
