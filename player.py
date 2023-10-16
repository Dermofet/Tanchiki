import pygame
import bullet as bul

WIDTH = 800
HEIGHT = 650
WHITE = (255, 255, 255)


class MyTank(pygame.sprite.Sprite):
    def __init__(self, pos, my_photo, all_wall):
        pygame.sprite.Sprite.__init__(self)
        self.photo = my_photo
        self.image = self.photo[0]
        self.rect = self.image.get_rect()
        self.rect.center = (pos[0], pos[1])
        self.speedx = 0
        self.speedy = 0
        self.vector = 0
        self.action = 0
        self.all_wall = all_wall

    def update(self):
        self.speedx = 0
        self.speedy = 0

        if self.action == 1:
            self.speedy = -3
            self.image = self.photo[0]
            self.vector = 1
        elif self.action == 2:
            self.speedy = 3
            self.image = self.photo[1]
            self.vector = 2
        elif self.action == 3:
            self.speedx = 3
            self.image = self.photo[2]
            self.vector = 3
        elif self.action == 4:
            self.speedx = -3
            self.image = self.photo[3]
            self.vector = 4

        self.action = 0

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        self.check_wall(self.all_wall)

        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, HEIGHT)
        self.rect.right = min(self.rect.right, WIDTH)
        self.rect.left = max(self.rect.left, 0)

    def move(self, action):
        self.action = action

    def shoot(self, my_bullet, photo_bullet):
        if self.vector == 1:
            bullet = bul.Bullet([self.rect.centerx, self.rect.centery + 30], self.vector, photo_bullet[0])
            my_bullet.add(bullet)
        elif self.vector == 2:
            bullet = bul.Bullet([self.rect.centerx, self.rect.centery - 30], self.vector, photo_bullet[1])
            my_bullet.add(bullet)
        elif self.vector == 3:
            bullet = bul.Bullet([self.rect.centerx + 30, self.rect.centery], self.vector, photo_bullet[2])
            my_bullet.add(bullet)
        elif self.vector == 4:
            bullet = bul.Bullet([self.rect.centerx - 30, self.rect.centery], self.vector, photo_bullet[3])
            my_bullet.add(bullet)

    def check_wall(self, all_wall):
        collisions_wall = pygame.sprite.spritecollide(self, all_wall, False)
        for elem in collisions_wall:
            if self.rect.left < elem.rect.right and self.rect.centerx > elem.rect.centerx and self.vector == 4:
                self.rect.left = elem.rect.right
            elif self.rect.bottom > elem.rect.top and self.rect.centery < elem.rect.centery and self.vector == 2:
                self.rect.bottom = elem.rect.top
            elif self.rect.right > elem.rect.left and self.rect.centerx < elem.rect.centerx and self.vector == 3:
                self.rect.right = elem.rect.left
            elif self.rect.top < elem.rect.bottom and self.rect.centery > elem.rect.centery and self.vector == 1:
                self.rect.top = elem.rect.bottom
