import pygame

BLACK = (0, 0, 0)
WIDTH = 800
HEIGHT = 650
BULLET_SPEED = 15


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, vector, photo):
        pygame.sprite.Sprite.__init__(self)
        self.image = photo
        self.rect = self.image.get_rect()
        self.rect.center = (pos[0], pos[1])
        self.vector = vector
        self.speed = BULLET_SPEED

    def update(self):
        if self.vector == 1:
            self.rect.y -= self.speed
        elif self.vector == 2:
            self.rect.y += self.speed
        elif self.vector == 3:
            self.rect.x += self.speed
        elif self.vector == 4:
            self.rect.x -= self.speed

        if self.rect.top < 0:
            self.kill()
        if self.rect.bottom > HEIGHT:
            self.kill()
        if self.rect.right > WIDTH:
            self.kill()
        if self.rect.left < 0:
            self.kill()
