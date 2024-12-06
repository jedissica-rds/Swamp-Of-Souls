import pygame
import sys
from ffpyplayer.player import MediaPlayer

class History2Screen:
    def __init__(self):
        # Inicializa Pygame
        pygame.init()

        # Clock
        self.clock = pygame.time.Clock()
        self.FPS = 40

        # Dimensões da tela
        self.WIDTH, self.HEIGHT = 1320, 680
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Swamp of Souls")

        # Carrega o vídeo sem áudio para evitar conflitos
        self.video_path = './assets/videos/intervalo2.mp4'
        self.player = MediaPlayer(self.video_path, ff_opts={'an': True})

    # Função para obter o frame atual do vídeo
    def get_frame(self, player):
        frame, val = player.get_frame()
        if val != 'eof' and frame is not None:
            img, t = frame
            img_surface = pygame.image.frombuffer(img.to_bytearray()[0], (img.get_size()), "RGB")
            return pygame.transform.scale(img_surface, (self.WIDTH, self.HEIGHT)), val
        return None, val

    def run(self):
        running = True

        while running:
            self.screen.fill((0, 0, 0))  # Tela preta como fundo inicial

            # Manipulação de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    # Se necessário, adicione qualquer resposta para pressionamento de tecla
                    pass

            # Obtém o frame atual do vídeo
            frame, val = self.get_frame(self.player)
            if frame:
                self.screen.blit(frame, (0, 0))
            elif val == 'eof':  # Verifica se o vídeo chegou ao final
                running = False

            # Atualiza a tela e limita o FPS
            pygame.display.update()
            self.clock.tick(self.FPS)
