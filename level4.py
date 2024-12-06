import pygame
import time
import constants as constant
import math
import level
import player as player_mod

# Initializing Pygame
pygame.init()

# Clock
clock = pygame.time.Clock()
FPS = 60

# Screen dimension
game_screen = pygame.display.set_mode((constant.WIDTH, constant.HEIGHT))
pygame.display.set_caption("Swamp of Souls")

# Player sprite
moving_sprites = pygame.sprite.Group()
player = player_mod.Player(constant.WIDTH/2 - 65, 370, "Right")
moving_sprites.add(player)

# players sounds
background_sound = pygame.mixer.Sound('assets/witch-forest-atmo-24654.mp3')
bridge_stability_sound = pygame.mixer.Sound('assets/wood-creaking.mp3')
click_sound = pygame.mixer.Sound('assets/click-keyboard.mp3')
background_sound.set_volume(0.5)  # Define o volume para 50%
background_sound.play()


class LevelFourScreen(level.Level):
    def __init__(self):
        super().__init__()
        self.running = True
        self.background_image = pygame.image.load('assets/background-sky.png').convert()
        self.gameover_img = pygame.image.load('assets/GAMEOVER4.png').convert()
        self.bg_w = self.background_image.get_width()
        self.tiles = math.ceil(constant.WIDTH / self.bg_w) + 1
        self.total_planks = 45
        self.crossed_planks = 0
        self.errors = 0
        self.max_errors = 5
        self.start_time = time.time()
        self.time_limit = 3
        self.letter_row = self.create_letter_row('assets/LetterRow.txt')
        self.bridge_stability = 100  # The percentage of stability of the bridge
        self.error_time = None  # Time when an error occurs
        self.error_color_duration = 0.4  # Duration in seconds to show the red color
        self.moon = pygame.transform.scale(pygame.image.load('assets/objects/moon.png').convert_alpha(), (102, 100))
        self.plank_positions = [(i * 69, constant.HEIGHT // 2 + 200) for i in range(self.total_planks)]
        self.player_position = [self.plank_positions[0][0], self.plank_positions[0][1] - 200]

    def render_text_with_alpha(self, text, font, color, alpha):
        text_surface = font.render(text, True, color)
        text_surface = text_surface.set_alpha(text_surface, alpha)
        return text_surface

    def player_jump(self, target_x, target_y, offset_x, stability_y):
        jump_peak = -100  # Altura máxima do pulo (negativo para subir)
        jump_duration = 10  # Duração total do pulo (número de frames)

        start_x, start_y = self.player_position[0], self.player_position[1]

        # Se o jogador está próximo do final da tela, altera o comportamento
        if self.player_position[0] > constant.WIDTH - 300:
            for i in range(jump_duration):
                # Progresso do pulo de 0 a 1
                t = i / jump_duration
                # Movimento vertical parabólico: o y diminui para o jogador subir
                parabola = 4 * jump_peak * t * (1 - t)
                self.player_position[1] = start_y + (target_y - start_y) * t + parabola

                # Desenha o estado atual do jogo para cada frame do pulo
                game_screen.fill(constant.BLACK)
                for i in range(0, self.tiles):
                    game_screen.blit(self.background_image, (i * self.bg_w + self.scroll, 0))
                # Scroll background
                self.scroll -= 1
                # Reset scroll
                if abs(self.scroll) > self.bg_w:
                    self.scroll = 0
                self.draw_bridge(offset_x, stability_y)
                self.draw_game_state(offset_x, stability_y)
                pygame.display.flip()
                pygame.time.delay(20)
        else:
            # Movimento de pulo normal
            for i in range(jump_duration):
                # Progresso do pulo de 0 a 1
                t = i / jump_duration

                # Movimento horizontal linear: interpolação de posição x
                self.player_position[0] = start_x + (target_x - start_x) * t

                # Movimento vertical parabólico: o y diminui para o jogador subir
                parabola = 4 * jump_peak * t * (1 - t)
                self.player_position[1] = start_y + (target_y - start_y) * t + parabola

                # Desenha o estado atual do jogo para cada frame do pulo
                game_screen.fill(constant.BLACK)
                for i in range(0, self.tiles):
                    game_screen.blit(self.background_image, (i * self.bg_w + self.scroll, 0))
                # Scroll background
                self.scroll -= 1
                # Reset scroll
                if abs(self.scroll) > self.bg_w:
                    scroll = 0
                self.draw_bridge(offset_x, stability_y)
                self.draw_game_state(offset_x, stability_y)
                pygame.display.flip()
                pygame.time.delay(20)

    def draw_bridge(self, offset_x, stability_y):
        # Draw all bridge planks based on displacement
        for i in range(self.total_planks):
            image = pygame.transform.scale(pygame.image.load('assets/plank.png').convert_alpha(), (75, 123))
            game_screen.blit(image, (self.plank_positions[i][0] + offset_x, self.plank_positions[i][1] + stability_y))
        floor = pygame.transform.scale(pygame.image.load('assets/floor.png').convert_alpha(), (320, 250))
        game_screen.blit(floor, (self.plank_positions[self.total_planks - 1][0] + offset_x + 75, self.plank_positions[self.total_planks - 1][1]))


    def draw_game_state(self, offset_x, stability_y):
        shadow_offset = 2
        player_img = pygame.transform.scale(player.image, (112, 200))
        game_screen.blit(player_img,
                         (self.player_position[0] + offset_x - 37, self.player_position[1] + stability_y + 45))
        game_screen.blit(self.moon, (605, 53))

        level_text = constant.normal_font.render(f'Level 4', True, constant.WHITE)
        game_screen.blit(level_text, (constant.WIDTH // 2 - 50, 20))

        center_x = constant.WIDTH // 2
        for i, letter in enumerate(self.letter_row):
            letter_color = constant.RED if i == 0 and self.error_time and time.time() - self.error_time < self.error_color_duration else constant.WHITE
            letter_surface = constant.font.render(letter, True, letter_color)
            x_position = center_x + (i * 100)
            shadow_text = constant.font.render(letter, True, (50, 50, 50))
            game_screen.blit(shadow_text, (x_position + shadow_offset, (constant.HEIGHT / 2) - 50 + shadow_offset))
            game_screen.blit(letter_surface, (x_position, constant.HEIGHT // 2 - 50))

        plank_text = constant.small_font.render(f'Tábuas atravessadas: {self.crossed_planks}', True, constant.WHITE)
        game_screen.blit(plank_text, (180, 30))
        error_text = constant.small_font.render(f'Erros: {self.errors}/{self.max_errors}', True, constant.BROWN)
        game_screen.blit(error_text, (180, 60))
        stability_text = constant.small_font.render(f'Estabilidade da ponte: {self.bridge_stability}%', True, constant.WHITE)
        game_screen.blit(stability_text, (180, 90))

        if len(self.letter_row) > 0:
            image_letter = pygame.transform.scale(
                pygame.image.load(
                    f'./assets/keys/key_{self.letter_row[0].upper().replace(" ", "")}.png').convert_alpha(),
                (100, 100))
            game_screen.blit(image_letter,(30,30))

    def run(self):
        running = True
        offset_x = 0  # Screen scroll control
        stability_y = 0

        while running:
            game_screen.fill(constant.WHITE)
            clock.tick(FPS)
            game_screen.fill(constant.BLACK)
            for i in range(0, self.tiles):
                game_screen.blit(self.background_image, (i * self.bg_w + self.scroll, 0))

            # Scroll background
            self.scroll -= 1

            # Reset scroll
            if abs(self.scroll) > self.bg_w:
                self.scroll = 0

            # Draw bridge and game state with offset
            self.draw_bridge(offset_x, stability_y)
            self.draw_game_state(offset_x, stability_y)

            # Check events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    click_sound.play()
                    # Check if the key pressed
                    if event.unicode.upper() == self.letter_row[0].upper():
                        # Correct letter, advance on the bridge
                        self.crossed_planks += 1
                        self.letter_row.pop(0)  # Remove the first letter
                        self.start_time = time.time()
                        # Move the player to the next plank
                        if self.crossed_planks < self.total_planks:
                            self.player_jump(self.plank_positions[self.crossed_planks][0] + 12,
                                        self.plank_positions[self.crossed_planks][1] - 200 + 45, offset_x, stability_y)

                        # Move the bridge
                        if self.player_position[0] > constant.WIDTH - 300:
                            offset_x = constant.WIDTH - 300 - self.player_position[0]
                    else:
                        # Incorrect letter, bridge gives a little
                        self.errors += 1
                        self.bridge_stability -= 20  # The bridge gives 20% for each error
                        stability_y += 30
                        self.error_time = time.time()  # Record the time of the error
                        bridge_stability_sound.play()

            # Check the time
            elapsed_time = time.time() - self.start_time
            if elapsed_time > self.time_limit:
                self.bridge_stability -= 10  # Player delay
                stability_y += 10
                self.start_time = time.time()
                bridge_stability_sound.play()

            # Check fault conditions
            if self.bridge_stability <= 0 or self.errors >= self.max_errors:
                self.show_game_over_screen(self.gameover_img)  # Exibe a tela de "game over" antes de reiniciar
                self.crossed_planks = 0
                self.errors = 0
                self.bridge_stability = 100
                self.letter_row = self.create_letter_row('assets/LetterRow.txt')
                player_position = [self.plank_positions[0][0] - 60, self.plank_positions[0][1] - 200]
                offset_x = 0
                stability_y = 0
                self.start_time = time.time()

            # Check if the player crossed all the boards
            if self.crossed_planks >= self.total_planks:
                # Move the player to the floor
                self.player_position[0] += 5
                player.animate()
            else:
                player.stopAnimating()

            time_bar_width = int(100 * max(0, (self.time_limit - elapsed_time) / self.time_limit))
            pygame.draw.rect(game_screen, constant.GRAY, (10, constant.HEIGHT - 90, time_bar_width, 20))

            if self.player_position[0] > constant.WIDTH:  # If the player has already left the screen
                running = False  # End the game

            # self.darken_screen()
            moving_sprites.update(0.25)
            pygame.display.flip()
            pygame.display.update()
