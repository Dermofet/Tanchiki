import pygame
import random
import bullet as bul

BLACK = (0, 0, 0)
WIDTH = 800
HEIGHT = 650


class EnemyTank(pygame.sprite.Sprite):
    def __init__(self, pos, all_wall, enemy_bullet):
        pygame.sprite.Sprite.__init__(self)
        self.photo1 = pygame.image.load('tank_enemy1.png').convert()
        self.photo1 = pygame.transform.scale(self.photo1, (50, 50))
        self.photo1.set_colorkey(BLACK)
        self.photo2 = pygame.image.load('tank_enemy3.png').convert()
        self.photo2 = pygame.transform.scale(self.photo2, (50, 50))
        self.photo2.set_colorkey(BLACK)
        self.photo3 = pygame.image.load('tank_enemy4.png').convert()
        self.photo3 = pygame.transform.scale(self.photo3, (50, 50))
        self.photo3.set_colorkey(BLACK)
        self.photo4 = pygame.image.load('tank_enemy2.png').convert()
        self.photo4 = pygame.transform.scale(self.photo4, (50, 50))
        self.photo4.set_colorkey(BLACK)
        self.image = self.photo1
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
            self.shoot(self.enemy_bullet)
            self.time_shoot = 0

        if self.vector == 1:
            self.speedy = -3
            self.set_image1()
        elif self.vector == 2:
            self.speedy = 3
            self.set_image2()
        elif self.vector == 3:
            self.speedx = -3
            self.set_image3()
        elif self.vector == 4:
            self.speedx = 3
            self.set_image4()

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

    def set_image1(self):
        self.image = self.photo1

    def set_image2(self):
        self.image = self.photo2

    def set_image3(self):
        self.image = self.photo3

    def set_image4(self):
        self.image = self.photo4

    def shoot(self, enemy_bullet):
        if self.vector == 1:
            bullet = bul.Bullet([self.rect.centerx, self.rect.centery + 30], self.vector, 'images/bullet1.png')
            enemy_bullet.add(bullet)
        elif self.vector == 2:
            bullet = bul.Bullet([self.rect.centerx, self.rect.centery - 30], self.vector, 'images/bullet3.png')
            enemy_bullet.add(bullet)
        elif self.vector == 3:
            bullet = bul.Bullet([self.rect.centerx - 30, self.rect.centery], self.vector, 'images/bullet4.png')
            enemy_bullet.add(bullet)
        elif self.vector == 4:
            bullet = bul.Bullet([self.rect.centerx + 30, self.rect.centery], self.vector, 'images/bullet2.png')
            enemy_bullet.add(bullet)

    def check_wall(self, all_wall):
        collisions_wall = pygame.sprite.spritecollide(self, all_wall, False)
        for elem in collisions_wall:
            if self.rect.left < elem.rect.right and self.rect.centerx > elem.rect.centerx and self.vector == 3:
                self.rect.left = elem.rect.right
            elif self.rect.bottom > elem.rect.top and self.rect.centery < elem.rect.centery and self.vector == 2:
                self.rect.bottom = elem.rect.top
            elif self.rect.right > elem.rect.left and self.rect.centerx < elem.rect.centerx and self.vector == 4:
                self.rect.right = elem.rect.left
            elif self.rect.top < elem.rect.bottom and self.rect.centery > elem.rect.centery and self.vector == 1:
                self.rect.top = elem.rect.bottom
