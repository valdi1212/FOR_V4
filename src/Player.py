import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, dx, dy, image, window):
        pygame.sprite.Sprite.__init__(self)
        self.imageMaster = image
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = dx
        self.rect.y = dy
        self.window = window

        self.alive = True
        self.dir = 0

    def update(self):
        old_center = self.rect.center
        self.image = pygame.transform.rotate(self.imageMaster, self.dir)
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def rotate_left(self):
        self.dir += 90
        if self.dir == 360:
            self.dir = 0

    def rotate_right(self):
        if self.dir == 0:
            self.dir = 270
        else:
            self.dir -= 90
