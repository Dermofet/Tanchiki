import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, photo):
        pygame.sprite.Sprite.__init__(self)
        self.image = photo
        self.rect = self.image.get_rect()
        self.rect.center = (pos[0], pos[1])
