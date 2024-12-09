import pygame

from history.ComingSoonScreen import ComingSoonScreen
from menu_class import SwampOfSoulsScreen, small_font
from intervals.interval1 import IntervalScreen
from intervals.interval2 import Interval2Screen
from intervals.interval3 import Interval3Screen
from intervals.interval4 import Interval4Screen
from levels.level2 import LevelTwoScreen
from levels.level1 import LevelOneScreen
from levels.level3 import LevelThreeOnScreen
from levels.level4 import LevelFourScreen
from levels.level5 import LevelFiveOnScreen
from history.history import HistoryScreen
from history.history_level2_1 import History2Screen
from history.history_level2_2 import History22Screen

# Inicializar o pygame
pygame.init()

# Definir as dimensões da tela
WIDTH, HEIGHT = 1320, 680
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Cria a tela (game_screen)
pygame.display.set_caption("Swamp of Souls")

# Função principal
def main():
    # Inicializar o menu
    menu_screen = SwampOfSoulsScreen()  # Passa a tela para o menu
    menu_screen.run()  # Executa o menu

    history = HistoryScreen()
    history.run()
    #
    # # Após o menu, inicializa o jogo
    game_screen = IntervalScreen()  # Inicializa o jogo
    game_screen.run()  # Executa o jogo


    level_screen = LevelOneScreen(WIDTH, HEIGHT, 100, small_font)
    level_screen.run()
    #
    game_screen = Interval2Screen()
    game_screen.run()
    # #
    history = History2Screen()
    history.run()
    # #
    level_screen = LevelTwoScreen(WIDTH, HEIGHT, 100, small_font)
    level_screen.run()
    # #
    history = History22Screen()
    history.run()
    # #
    game_screen = Interval3Screen()
    game_screen.run()
    # #
    level_screen = LevelThreeOnScreen(WIDTH, HEIGHT, 100, small_font)
    level_screen.run()
    #
    game_screen = Interval4Screen()
    game_screen.run()
    #
    level_screen = LevelFourScreen(WIDTH, HEIGHT, 100, small_font)
    level_screen.run()
    #
    level_screen = LevelFiveOnScreen(WIDTH, HEIGHT, 100, small_font)
    level_screen.run()
    #
    history_screen = ComingSoonScreen()
    history_screen.run()

if __name__ == '__main__':
    main()
