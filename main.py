import pygame
import random

WIDTH = 800
HEIGHT = 650
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class Wall(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('wall.png').convert()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (pos[0], pos[1])


class MyTank(pygame.sprite.Sprite):
    def __init__(self, pos, all_wall):
        pygame.sprite.Sprite.__init__(self)
        self.photo1 = pygame.image.load('my_tank1.png').convert()
        self.photo1 = pygame.transform.scale(self.photo1, (50, 50))
        self.photo1.set_colorkey(WHITE)
        self.photo2 = pygame.image.load('my_tank3.png').convert()
        self.photo2 = pygame.transform.scale(self.photo2, (50, 50))
        self.photo2.set_colorkey(WHITE)
        self.photo3 = pygame.image.load('my_tank4.png').convert()
        self.photo3 = pygame.transform.scale(self.photo3, (50, 50))
        self.photo3.set_colorkey(WHITE)
        self.photo4 = pygame.image.load('my_tank2.png').convert()
        self.photo4 = pygame.transform.scale(self.photo4, (50, 50))
        self.photo4.set_colorkey(WHITE)
        self.image = self.photo1
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)
        self.rect.center = (pos[0], pos[1])
        self.speedx = 0
        self.speedy = 0
        self.vector = 0
        self.keys = pygame.key.get_pressed()
        self.all_wall = all_wall


    def update(self):
        self.speedx = 0
        self.speedy = 0

        if self.keys[pygame.K_UP]:
            self.speedy = -3
            self.set_image1()
            self.vector = 1
        elif self.keys[pygame.K_DOWN]:
            self.speedy = 3
            self.set_image2()
            self.vector = 2
        elif self.keys[pygame.K_LEFT]:
            self.speedx = -3
            self.set_image3()
            self.vector = 3
        elif self.keys[pygame.K_RIGHT]:
            self.speedx = 3
            self.set_image4()
            self.vector = 4

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

    def shoot(self, my_bullet):
        if self.vector == 1:
            bullet = Bullet([self.rect.centerx, self.rect.centery + 30], self.vector, 'bullet1.png')
            my_bullet.add(bullet)
        elif self.vector == 2:
            bullet = Bullet([self.rect.centerx, self.rect.centery - 30], self.vector, 'bullet3.png')
            my_bullet.add(bullet)
        elif self.vector == 3:
            bullet = Bullet([self.rect.centerx - 30, self.rect.centery], self.vector, 'bullet4.png')
            my_bullet.add(bullet)
        elif self.vector == 4:
            bullet = Bullet([self.rect.centerx + 30, self.rect.centery], self.vector, 'bullet2.png')
            my_bullet.add(bullet)

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
            bullet = Bullet([self.rect.centerx, self.rect.centery + 30], self.vector, 'bullet1.png')
            enemy_bullet.add(bullet)
        elif self.vector == 2:
            bullet = Bullet([self.rect.centerx, self.rect.centery - 30], self.vector, 'bullet3.png')
            enemy_bullet.add(bullet)
        elif self.vector == 3:
            bullet = Bullet([self.rect.centerx - 30, self.rect.centery], self.vector, 'bullet4.png')
            enemy_bullet.add(bullet)
        elif self.vector == 4:
            bullet = Bullet([self.rect.centerx + 30, self.rect.centery], self.vector, 'bullet2.png')
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


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, vector, photo):
        pygame.sprite.Sprite.__init__(self)
        self.photo1 = pygame.image.load(photo).convert()
        self.photo1 = pygame.transform.scale(self.photo1, (10, 10))
        self.photo1.set_colorkey(BLACK)
        self.image = self.photo1
        self.rect = self.image.get_rect()
        self.rect.center = (pos[0], pos[1])
        self.vector = vector
        self.speed = 15

    def update(self):
        if self.vector == 1:
            self.rect.y -= self.speed
        elif self.vector == 2:
            self.rect.y += self.speed
        elif self.vector == 3:
            self.rect.x -= self.speed
        elif self.vector == 4:
            self.rect.x += self.speed

        if self.rect.top < 0:
            self.kill()
        if self.rect.bottom > HEIGHT:
            self.kill()
        if self.rect.right > WIDTH:
            self.kill()
        if self.rect.left < 0:
            self.kill()


def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Танчики")
    clock = pygame.time.Clock()

    all_wall = pygame.sprite.Group()
    for wall in [[300, 500], [225, 500], [150, 500], [25, 75], [75, 75]]:
        all_wall.add(Wall(wall))
    my_bullet = pygame.sprite.Group()
    enemy_bullet = pygame.sprite.Group()
    my_tank = pygame.sprite.Group()
    player = MyTank([375, 625], all_wall)
    my_tank.add(player)
    enemy_tanks = pygame.sprite.Group()
    for tank in [[25, 25], [400, 0], [775, 0]]:
        enemy_tanks.add(EnemyTank(tank, all_wall, enemy_bullet))

    running = True
    while running:
        # Держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)
        for event in pygame.event.get():
            # check for closing window
            keys = pygame.key.get_pressed()
            player.keys = keys
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot(my_bullet)

        pygame.sprite.groupcollide(my_bullet, enemy_tanks, True, True)
        if pygame.sprite.groupcollide(enemy_bullet, my_tank, True, True):
            running = False
        pygame.sprite.groupcollide(my_bullet, all_wall, True, True)
        pygame.sprite.groupcollide(enemy_bullet, all_wall, True, True)

        my_tank.update()
        enemy_tanks.update()
        all_wall.update()
        my_bullet.update()
        enemy_bullet.update()

        screen.fill(BLACK)
        my_tank.draw(screen)
        enemy_tanks.draw(screen)
        all_wall.draw(screen)
        my_bullet.draw(screen)
        enemy_bullet.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
