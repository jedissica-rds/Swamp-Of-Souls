import pygame
import sys

class ComingSoonScreen:
    def __init__(self):
        # Initializing Pygame
        pygame.init()

        # Clock
        self.clock = pygame.time.Clock()
        self.FPS = 40

        # Screen dimensions
        self.WIDTH, self.HEIGHT = 1320, 680
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Swamp of Souls")

        # Background and images
        self.bg_image = pygame.image.load('assets/tutorials/Coming Soon Scene.png').convert_alpha()
        self.current_bg = self.bg_image

        # Timer and effect durations
        self.wait_time = 3000           # 5 seconds to show the first image before fade
        self.fade_in_duration = 2000
        self.appear_delay = 2000
        self.start_time = pygame.time.get_ticks()
        self.alpha = 0                 # Initial opacity for fade-out

        # Sound effects
        self.background_sound = pygame.mixer.Sound('assets/sounds-effects/Exploring Nightmare.wav')
        self.click_sound = pygame.mixer.Sound('assets/click-keyboard.mp3')
        self.background_sound.set_volume(0.6)
        self.background_sound.play()

        # State tracking
        self.is_waiting = False
        self.is_fading_in = True
        self.is_displaying = False

    def run(self):
        running = True

        while running:
            self.screen.fill((0, 0, 0))  # start with black backgorund

            current_time = pygame.time.get_ticks()

            # fade in control
            if self.is_fading_in:
                if current_time - self.start_time >= self.appear_delay:
                    self.alpha += (255 / (self.fade_in_duration / self.FPS))
                    if self.alpha >= 255:
                        self.alpha = 255
                        self.is_fading_in = False
                        self.is_displaying = True
                        self.start_time = current_time

            # show the image if is not in fade in
            if self.is_displaying:
                if current_time - self.start_time >= self.wait_time:
                    running = False
                else:
                    faded_bg = self.bg_image.copy()
                    faded_bg.set_alpha(self.alpha)
                    self.screen.blit(faded_bg, (-90, 0))

            if self.is_fading_in:
                faded_bg = self.bg_image.copy()
                faded_bg.set_alpha(self.alpha)
                self.screen.blit(faded_bg, (-90, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.click_sound.play()
                    running = False

            pygame.display.update()
            self.clock.tick(self.FPS)

        # stop the music when exits
        self.background_sound.stop()

