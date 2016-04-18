import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, dx, dy, image, window):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = dx
        self.rect.y = dy
        self.window = window

        self.alive = True
