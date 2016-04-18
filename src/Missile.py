import pygame


class Missile(pygame.sprite.Sprite):
    def __init__(self, image, dir=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotate(image, dir)
        self.rect = self.image.get_rect()
        self.dir = dir

    def fly(self):
        if self.dir == 0:
            self.rect.y -= 5
        elif self.dir == 90:
            self.rect.x -= 5
        elif self.dir == 180:
            self.rect.y += 5
        elif self.dir == 270:
            self.rect.x += 5
