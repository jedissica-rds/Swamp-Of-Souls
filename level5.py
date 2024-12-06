import pygame
import sys
import time
import player as player_mod
import random
import constants as constant
import level

# Configurações da janela
pygame.init()
screen = pygame.display.set_mode((constant.WIDTH, constant.HEIGHT))
pygame.display.set_caption("Swamp of Souls")

# Background and images
bg_images = []
for i in range(2, 6):
    bg_image = pygame.image.load(f'assets/background/BG_{i}.png').convert_alpha()
    bg_images.append(bg_image)
bg_width = bg_images[0].get_width()

static_bg_image = pygame.image.load(f'assets/background/BG_1.png').convert_alpha()

# Player sprite
moving_sprites = pygame.sprite.Group()
player = player_mod.Player(constant.WIDTH / 2, 370, "Right")
moving_sprites.add(player)

# Fonte e frases
phrases = ["Os dias naquela cabana eram interminaveis, e sua presença era tudo o que eu conhecia.", "Nao foi minha culpa, era o que precisava ser feito.",
           "Nos eramos iguais em tudo, mesmas manias, mesmos sorrisos, mesma dor, mesma fome...", "E no fim, tudo fazia sentido...", "Eu nunca a deixei partir; talvez, na escuridao, eu apenas tenha permitido que algo a mais tomasse meu lugar..."]

wendigo_image = pygame.transform.scale(pygame.image.load(
    f'./assets/wendigo.png').convert_alpha(),
    (587, 412))

# Sounds
background_sound = pygame.mixer.Sound('assets/sounds-effects/Close Encounter 1.wav')
background_sound.set_volume(0.7)
background_sound.play(loops=-1)

preframe1 = pygame.transform.scale(pygame.image.load('assets/backgrounds/FASE 5.png').convert_alpha(),(1320,680))
preframe2 = pygame.transform.scale(pygame.image.load('assets/backgrounds/FASE 5-1.png').convert_alpha(),(1320,680))
preframe3 = pygame.transform.scale(pygame.image.load('assets/backgrounds/FASE 5-2.png').convert_alpha(),(1320,680))
preframe4 = pygame.transform.scale(pygame.image.load('assets/backgrounds/FASE 5-3.png').convert_alpha(),(1320,680))

frame1 = pygame.transform.scale(pygame.image.load('assets/backgrounds/FASE 5 - POS.png').convert_alpha(),(1320,680))
frame2 = pygame.transform.scale(pygame.image.load('assets/backgrounds/FASE 5 - POS-1.png').convert_alpha(),(1320,680))
frame3 = pygame.transform.scale(pygame.image.load('assets/backgrounds/FASE 5 - POS-2.png').convert_alpha(),(1320,680))
frame4 = pygame.transform.scale(pygame.image.load('assets/backgrounds/FASE 5 - POS-3.png').convert_alpha(),(1320,680))
frame5 = pygame.transform.scale(pygame.image.load('assets/backgrounds/FASE 5 - POS-4.png').convert_alpha(),(1320,680))


class LevelFiveOnScreen(level.Level):
    def __init__(self):
        super().__init__()
        self.current_phrase_index = 0
        self.typed_text = ""
        self.errors = 0
        self.enemy_approach_count = 0
        self.enemy_position = 0
        self.max_approach = 12
        self.interval_duration = random.randint(2,5)
        self.typing_duration_limit = 10
        self.max_errors = 8
        self.game_over = False
        self.interval_start_time = time.time()
        self.typing_start_time = None
        self.letter = '0'
        self.line_width = 800  # Largura máxima para a quebra de linha

    # Função para renderizar o texto com quebra de linha
    def render_text_multiline(self, text, color, x, y, max_width):
        words = text.split()
        lines = []
        current_line = ""

        # Agrupa palavras para criar linhas que respeitem a largura máxima
        for word in words:
            test_line = current_line + ("" if current_line == "" else " ") + word
            test_surface = constant.small_font.render(test_line, True, color)

            if test_surface.get_width() <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        # Renderiza cada linha com espaçamento vertical
        for i, line in enumerate(lines):
            line_surface = constant.small_font.render(line, True, color)
            screen.blit(line_surface, (x, y + i * constant.small_font.get_height()))

    def render_text(self, text, color, x, y):
        surface = constant.small_font.render(text, True, color)
        screen.blit(surface, (x, y))

    def show_interval_bar(self):
        self.elapsed = time.time() - self.interval_start_time
        if self.elapsed >= self.interval_duration:
            return False
        pygame.draw.rect(screen, constant.GRAY, [100, 300, (self.elapsed / self.interval_duration) * 1100, 20])
        return True

    def show_pos_frames_screen(self):
        screen.fill(constant.WHITE)
        screen.blit(frame1, (0, 0))
        pygame.display.update()
        time.sleep(3)  # Pausa por 2 segundos
        screen.fill(constant.WHITE)
        screen.blit(frame2, (0, 0))
        pygame.display.update()
        time.sleep(3)
        screen.fill(constant.WHITE)
        screen.blit(frame3, (0, 0))
        pygame.display.update()
        time.sleep(3)
        screen.fill(constant.WHITE)
        screen.blit(frame4, (0, 0))
        pygame.display.update()
        time.sleep(3)  # Pausa por 2 segundos
        screen.fill(constant.WHITE)
        screen.blit(frame5, (0, 0))
        pygame.display.update()
        time.sleep(2)

    def show_pre_frames_screen(self):
        screen.fill(constant.WHITE)
        screen.blit(preframe1, (-10, 0))
        pygame.display.update()
        time.sleep(3)  # Pausa por 2 segundos
        screen.fill(constant.WHITE)
        screen.blit(preframe2, (-10, 0))
        pygame.display.update()
        time.sleep(3)
        screen.fill(constant.WHITE)
        screen.blit(preframe3, (-10, 0))
        pygame.display.update()
        time.sleep(3)
        screen.fill(constant.WHITE)
        screen.blit(preframe4, (-10, 0))
        pygame.display.update()
        time.sleep(3)

    def flash_screen(self):
        screen.fill(constant.WHITE)
        pygame.display.flip()
        pygame.time.delay(50)  # Tempo do flash em milissegundos

    def start_typing(self):
        self.typing_start_time = time.time()
        self.typed_text = ""
        self.errors = 0
        self.letter = phrases[self.current_phrase_index][0]

    def check_typing_accuracy(self, event):
        if self.typing_start_time is None:
            self.typing_start_time = time.time()

        if event.key == pygame.K_BACKSPACE:
            self.typed_text = self.typed_text[:-1]
        elif event.unicode.isprintable():
            self.typed_text += event.unicode
            correct_text = phrases[self.current_phrase_index][:len(self.typed_text)]
            if len(self.typed_text) < len(phrases[self.current_phrase_index]):
                self.letter = phrases[self.current_phrase_index][len(self.typed_text)]
            else:
                self.letter = '0'
            if self.typed_text == correct_text:
                pass  # Tudo correto até agora
            else:
                self.errors += 1

            # Verifica limite de tempo para digitar uma letra
            if time.time() - self.typing_start_time > self.typing_duration_limit:
                self.enemy_approach_count += 1
                self.flash_screen()
                self.typing_start_time = time.time()


            # Aproxima o inimigo se erros ultrapassarem o limite
            if self.errors > self.max_errors:
                self.enemy_approach_count += 1
                self.errors = 0
                self.typing_start_time = time.time()
                self.flash_screen()  # Chama o flash toda vez que o Wendigo se aproxima

    def run(self):
        self.running = True
        self.show_pre_frames_screen()
        while self.running:
            player.animate()
            screen.fill(constant.WHITE)
            self.draw_background(static_bg_image)

            dark_overlay = pygame.Surface((constant.WIDTH, constant.HEIGHT))
            dark_overlay.set_alpha(150)
            dark_overlay.fill(constant.BLACK)
            screen.blit(dark_overlay, (0, 0))

            # Eventos do jogo
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and not self.game_over:
                    if self.interval_start_time and time.time() - self.interval_start_time < self.interval_duration:
                        continue
                    self.check_typing_accuracy(event)

            # Desenha a barra de intervalo e exibe a próxima frase após o intervalo
            if self.interval_start_time:
                if not self.show_interval_bar():
                    self.interval_start_time = None
                    self.start_typing()

            # Desenha o texto da frase atual com quebra de linha
            if not self.interval_start_time:
                self.render_text_multiline(phrases[self.current_phrase_index], constant.WHITE, 250, 150, self.line_width)

                # Renderiza o texto digitado com cores indicativas
                for i, char in enumerate(self.typed_text):
                    color = constant.GREEN if char == phrases[self.current_phrase_index][i] else constant.RED
                    self.render_text(char, color, 250 + i * 12, 250)

                # Passa para a próxima frase ao alcançar o final da frase atual
                if len(self.typed_text) == len(phrases[self.current_phrase_index]):
                    self.current_phrase_index += 1
                    if self.current_phrase_index >= len(phrases):
                        self.show_pos_frames_screen()
                    else:
                        self.interval_start_time = time.time()
                        self.start_typing()
                    # Verifica se ele acertou tudo
                    if self.typed_text == phrases[self.current_phrase_index - 1]:
                        self.enemy_approach_count -= 3
                    else:
                        self.enemy_approach_count -= 1

            # Desenha o inimigo na posição correta
            self.enemy_position = -550 + (constant.WIDTH / 2) * (self.enemy_approach_count / self.max_approach)
            screen.blit(wendigo_image, [self.enemy_position, 200])

            # Checa se o inimigo alcançou o jogador
            if self.enemy_approach_count >= self.max_approach:
                self.show_pos_frames_screen()
                self.running = False

            try:
                image_letter = pygame.transform.scale(
                    pygame.image.load(
                        f'./assets/keys/key_{self.letter.upper().replace(" ", "")}.png').convert_alpha(),
                    (100, 100)
                )
            except FileNotFoundError:
                image_letter = pygame.Surface((100, 100), pygame.SRCALPHA)
                image_letter.fill((255, 0, 0))  # Imagem em vermelho para indicar erro

            screen.blit(image_letter, (30, 30))

            level_text = constant.small_font.render(f"Level 5", True, constant.WHITE)
            screen.blit(level_text, (600, 10))

            plank_text = constant.small_font.render(f'Talvez repetindo, as memórias façam mais sentido...', True, constant.WHITE)
            screen.blit(plank_text, (150, 50))

            if player.isAnimating:
                self.scroll += 3
            if abs(self.scroll) > bg_width:
                self.scroll = 0
            elif abs(self.scroll) < 0:
                self.scroll = bg_width

            moving_sprites.draw(screen)
            moving_sprites.update(0.7)

            pygame.display.update()
            pygame.display.flip()
            pygame.time.Clock().tick(30)
