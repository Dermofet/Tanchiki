import pygame
import random
import bullet as bul

BLACK = (0, 0, 0)
WIDTH = 800
HEIGHT = 650


class EnemyTank(pygame.sprite.Sprite):
    def __init__(self, pos, photo, all_wall, enemy_bullet, photo_bullet):
        pygame.sprite.Sprite.__init__(self)
        self.photo_bullet = photo_bullet
        self.photo = photo
        self.image = self.photo[0]
        self.rect = self.image.get_rect()
        self.rect.center = (pos[0], pos[1])
        self.speedx = 0
        self.speedy = 0
        self.vector = 0
        self.time_move = 0
        self.time_shoot = 0
        self.all_wall = all_wall
        self.enemy_bullet = enemy_bullet

    def update(self):
        self.speedx = 0
        self.speedy = 0

        self.time_move += 1

        if self.time_move > 30:
            self.vector = random.randint(1, 4)
            self.time_move = 0

        self.time_shoot += 1

        if self.time_shoot > random.randint(60, 180):
            self.shoot(self.enemy_bullet, self.photo_bullet)
            self.time_shoot = 0

        if self.vector == 1:
            self.speedy = -3
            self.image = self.photo[0]
        elif self.vector == 2:
            self.speedy = 3
            self.image = self.photo[1]
        elif self.vector == 3:
            self.speedx = 3
            self.image = self.photo[2]
        elif self.vector == 4:
            self.speedx = -3
            self.image = self.photo[3]

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        self.check_wall(self.all_wall)

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self, enemy_bullet, photo_bullet):
        if self.vector == 1:
            bullet = bul.Bullet([self.rect.centerx, self.rect.centery + 30], self.vector, photo_bullet[0])
            enemy_bullet.add(bullet)
        elif self.vector == 2:
            bullet = bul.Bullet([self.rect.centerx, self.rect.centery - 30], self.vector, photo_bullet[1])
            enemy_bullet.add(bullet)
        elif self.vector == 3:
            bullet = bul.Bullet([self.rect.centerx + 30, self.rect.centery], self.vector, photo_bullet[2])
            enemy_bullet.add(bullet)
        elif self.vector == 4:
            bullet = bul.Bullet([self.rect.centerx - 30, self.rect.centery], self.vector, photo_bullet[3])
            enemy_bullet.add(bullet)

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
