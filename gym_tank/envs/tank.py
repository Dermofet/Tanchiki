import pygame
import gym
from gym import error, spaces, utils
from gym.utils import seeding

import enemy_tank as _enemy_tank
import wall as _wall
import player as _player

WIDTH = 800
HEIGHT = 650
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

def main():
    class FooEnv(gym.Env):
        metadata = {'render.modes': ['human']}

        def __init__(self):

            # Pygame init
            pygame.init()
            pygame.mixer.init()
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("Танчики")
            self.clock = pygame.time.Clock()

            # Walls init
            self.all_wall = pygame.sprite.Group()
            for wall in [[300, 500], [225, 500], [150, 500], [25, 75], [75, 75]]:
                self.all_wall.add(_wall.Wall(wall))

            # Player's bullets init
            self.my_bullet = pygame.sprite.Group()

            # Enemies' bullets init
            self.enemy_bullet = pygame.sprite.Group()

            # Player init
            self.my_tank = pygame.sprite.Group()
            self.player = _player.MyTank([375, 625], self.all_wall)
            self.my_tank.add(self.player)

            # Enemy tanks init
            self.enemy_tanks = pygame.sprite.Group()
            for tank in [[25, 25], [400, 0], [775, 0]]:
                self.enemy_tanks.add(_enemy_tank.EnemyTank(tank, self.all_wall, self.enemy_bullet))

        def step(self, action):
            self.clock.tick(FPS)

            if action == pygame.QUIT:
                self.close()
            elif action == pygame.K_SPACE:
                self.player.shoot(self.my_bullet)

            pygame.sprite.groupcollide(self.my_bullet, self.enemy_tanks, True, True)
            if pygame.sprite.groupcollide(self.enemy_bullet, self.my_tank, True, True):
                self.reset()
            pygame.sprite.groupcollide(self.my_bullet, self.all_wall, True, True)
            pygame.sprite.groupcollide(self.enemy_bullet, self.all_wall, True, True)

        def reset(self):
            ...

        def render(self, mode='human'):
            self.my_tank.update()
            self.enemy_tanks.update()
            self.all_wall.update()
            self.my_bullet.update()
            self.enemy_bullet.update()

            self.screen.fill(BLACK)
            self.my_tank.draw(self.screen)
            self.enemy_tanks.draw(self.screen)
            self.all_wall.draw(self.screen)
            self.my_bullet.draw(self.screen)
            self.enemy_bullet.draw(self.screen)

            pygame.display.flip()

        def close(self):
            pygame.quit()


if __name__ == '__main__':
    main()
