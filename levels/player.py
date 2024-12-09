import pygame
PLAYER_WIDTH = 32
PLAYER_HEIGHT = 64

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, orientation):
        super().__init__()

        self.sprites = []  # Walking sprites
        self.angle = 0
        self.orientation = orientation

        # Load walking sprites
        for i in range(1, 9):
            sprite = pygame.image.load(f'assets/walking/ALMA_WALKING{i}.png').convert_alpha()
            self.sprites.append(sprite)

        # Load idle and jar-holding sprites separately
        self.idle_sprite = pygame.image.load('assets/idle/ALMA.png').convert_alpha()
        self.holding_jar_sprite = pygame.image.load('assets/alma/ALMA_WITH_JAR.png').convert_alpha()

        # Load the catching sprite
        self.catching_sprite = pygame.image.load('assets/alma/ALMA_WITH_JAR_FULL.png').convert_alpha()
        self.isCatching = False  # Track if player is in catching state

        self.current_sprite = 0
        self.image = self.idle_sprite
        self.isAnimating = False
        self.isHoldingJar = False  # Track if player is holding the jar

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def animate(self):
        if not self.isHoldingJar:
            self.isAnimating = True

    def stopAnimating(self):
        self.isAnimating = False
        if self.isHoldingJar:
            self.image = self.holding_jar_sprite
        if self.isCatching:
            self.image = self.catching_sprite
        else:
            self.image = self.idle_sprite

    def grab_jar(self):
        self.isHoldingJar = True
        self.image = self.holding_jar_sprite  # Set to jar-holding sprite

    def catch_firefly(self):
        self.isCatching = True
        self.image = self.catching_sprite  # Change to catching image

    def flip_sprites(self):
        if self.orientation == "Right":
            self.image = pygame.transform.flip(self.image, False, False)
        elif self.orientation == "Left":
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, speed):
        if self.isAnimating and not self.isHoldingJar:
            self.current_sprite += speed
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0  # Loop back to start of walking sprites
                self.isAnimating = False
            self.image = self.sprites[int(self.current_sprite)]
        elif self.isHoldingJar:
            self.image = self.holding_jar_sprite  # Keep the jar-holding sprite when holding jar
            if self.isCatching:
                self.image = self.catching_sprite
        else:
            self.stopAnimating()  # Default to idle sprite when not animating

        self.flip_sprites()
