import pygame
import time

#Screen settings
width = 1320
height = 680
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
FPS = 60


class Block:
    def __init__(self, x, y, letter, ):
        self.rect = pygame.Rect(x, y, 75, 75)
        self.letter = letter
        self.is_seeing = True
        self.incorrect = False
        self.image = pygame.image.load('assets/Group 29 (1).png').convert_alpha()
        self.total_blocks = 10
        self.blocks_positions = [(i * 69, height // 2) for i in range(self.total_blocks)]

    def draw(self, camera):
        if self.is_seeing:
            pos = camera.apply(self.rect)
            screen.blit(self.image, pos)
            font = pygame.font.Font(None, 50)
            color = (255, 255, 255)
            if self.incorrect:
                color = (255, 0, 0)
            text1 = font.render(self.letter, True, (color))
            text_rect = text1.get_rect(center=(pos.centerx + 200 , pos.top - 10))
            screen.blit(text1, text_rect)

            if len(self.letter) > 0:
                image_letter = pygame.transform.scale(
                    pygame.image.load(
                        f'./assets/keys/key_{self.letter[0].upper().replace(" ", "")}.png').convert_alpha(),
                    (100, 100))
                screen.blit(image_letter,(30,30))

    def reset_block(self, x, y, letter):
        self.rect.topleft = (x, y)
        self.letter = letter
        self.is_seeing = True
        self.image = pygame.image.load('assets/Group 29 (1).png').convert_alpha()


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, rect):
        return rect.move(-self.camera.x, -self.camera.y)

    def update(self, target):
        x = -target.x + int(800 / 2)
        y = -target.y + int(600 / 2)
        x = min(0, x)
        y = max(0, y)
        x = max(-(self.width - 800), x)
        y = max((self.height - 600), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)