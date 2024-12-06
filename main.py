import pygame

from ComingSoonScreen import ComingSoonScreen
from menu_class import SwampOfSoulsScreen
from interval1 import IntervalScreen
from interval2 import Interval2Screen
from interval3 import Interval3Screen
from interval4 import Interval4Screen
from level2 import LevelTwoScreen
from level1 import LevelOneScreen
from level3 import LevelThreeOnScreen
from level4 import LevelFourScreen
from level5 import LevelFiveOnScreen
from history import HistoryScreen
from history_level2_1 import History2Screen
from history_level2_2 import History22Screen

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

    # Após o menu, inicializa o jogo
    game_screen = IntervalScreen()  # Inicializa o jogo
    game_screen.run()  # Executa o jogo


    level_screen = LevelOneScreen()
    level_screen.run()

    game_screen = Interval2Screen()
    game_screen.run()

    history = History2Screen()
    history.run()

    level_screen = LevelTwoScreen()
    level_screen.run()

    history = History22Screen()
    history.run()

    game_screen = Interval3Screen()
    game_screen.run()

    level_screen = LevelThreeOnScreen()
    level_screen.run()

    game_screen = Interval4Screen()
    game_screen.run()

    level_screen = LevelFourScreen()
    level_screen.run()

    level_screen = LevelFiveOnScreen()
    level_screen.run()

    history_screen = ComingSoonScreen()
    history_screen.run()

if __name__ == '__main__':
    main()
