import pygame

pygame.init()
# Defining colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
OFF_WHITE = (217, 249, 255)
RED = (100, 20, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BROWN = (123, 63, 0)

# Defining fonts
normal_font = pygame.font.Font("assets/font/IMFellEnglish-Regular.ttf", 36)
small_font = pygame.font.Font("assets/font/IMFellEnglish-Regular.ttf", 24)
smallest_font = pygame.font.Font("assets/font/IMFellEnglish-Regular.ttf", 12)
x_small_font = pygame.font.Font("assets/font/IMFellEnglish-Regular.ttf", 16)
font = pygame.font.Font(None, 100)

# Screen dimensions
WIDTH, HEIGHT = 1320, 680

click_sound = pygame.mixer.Sound('assets/sounds-effects/click-keyboard.mp3')