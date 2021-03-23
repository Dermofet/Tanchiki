import pygame
import gym
from random import choice

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Convolution2D
from tensorflow.keras.optimizers import Adam

from rl.agents import DQNAgent
from rl.memory import SequentialMemory
from rl.policy import LinearAnnealedPolicy, EpsGreedyQPolicy

import enemy_tank as _enemy_tank
import wall as _wall
import player as _player

WIDTH = 800
HEIGHT = 650
FPS = 30
BULLET_SPEED = 15

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


class TankEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.action_space = gym.spaces.Discrete(6)
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(HEIGHT, WIDTH, 3), dtype=np.uint8)

        # Pygame init
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Танчики")
        self.clock = pygame.time.Clock()

        # Play time (120 sec)
        self.time = FPS * 120

        # Walls init
        self.all_wall = pygame.sprite.Group()

        # Player's bullets init
        self.my_bullet = pygame.sprite.Group()

        # Enemies' bullets init
        self.enemy_bullet = pygame.sprite.Group()
        self.tanks = ((25, 25), (400, 25), (775, 25))

        # Player init
        self.my_tank = pygame.sprite.Group()
        self.player = None

        # Enemy tanks init
        self.enemy_tanks = pygame.sprite.Group()

        # Upload photos:

        # Wall
        self.photo_wall = pygame.image.load('images/wall.png').convert()
        self.photo_wall = pygame.transform.scale(self.photo_wall, (50, 50))

        # Player tank
        # UP
        self.photo_player_up = pygame.image.load('images/my_tank_up.png').convert()
        self.photo_player_up = pygame.transform.scale(self.photo_player_up, (50, 50))
        self.photo_player_up.set_colorkey(WHITE)
        # DOWN
        self.photo_player_down = pygame.image.load('images/my_tank_down.png').convert()
        self.photo_player_down = pygame.transform.scale(self.photo_player_down, (50, 50))
        self.photo_player_down.set_colorkey(WHITE)
        # RIGHT
        self.photo_player_right = pygame.image.load('images/my_tank_right.png').convert()
        self.photo_player_right = pygame.transform.scale(self.photo_player_right, (50, 50))
        self.photo_player_right.set_colorkey(WHITE)
        # LEFT
        self.photo_player_left = pygame.image.load('images/my_tank_left.png').convert()
        self.photo_player_left = pygame.transform.scale(self.photo_player_left, (50, 50))
        self.photo_player_left.set_colorkey(WHITE)

        self.photo_player = [self.photo_player_up, self.photo_player_down, self.photo_player_right,
                             self.photo_player_left]

        # Enemy tank
        # UP
        self.photo_enemy_tank_up = pygame.image.load('images/tank_enemy_up.png').convert()
        self.photo_enemy_tank_up = pygame.transform.scale(self.photo_enemy_tank_up, (50, 50))
        self.photo_enemy_tank_up.set_colorkey(BLACK)
        # DOWN
        self.photo_enemy_tank_down = pygame.image.load('images/tank_enemy_down.png').convert()
        self.photo_enemy_tank_down = pygame.transform.scale(self.photo_enemy_tank_down, (50, 50))
        self.photo_enemy_tank_down.set_colorkey(BLACK)
        # RIGHT
        self.photo_enemy_tank_right = pygame.image.load('images/tank_enemy_right.png').convert()
        self.photo_enemy_tank_right = pygame.transform.scale(self.photo_enemy_tank_right, (50, 50))
        self.photo_enemy_tank_right.set_colorkey(BLACK)
        # LEFT
        self.photo_enemy_tank_left = pygame.image.load('images/tank_enemy_left.png').convert()
        self.photo_enemy_tank_left = pygame.transform.scale(self.photo_enemy_tank_left, (50, 50))
        self.photo_enemy_tank_left.set_colorkey(BLACK)

        self.photo_enemy_tank = [self.photo_enemy_tank_up, self.photo_enemy_tank_down, self.photo_enemy_tank_right,
                                 self.photo_enemy_tank_left]

        # Bullet
        # UP
        self.photo_bullet_up = pygame.image.load("images/bullet_up.png").convert()
        self.photo_bullet_up = pygame.transform.scale(self.photo_bullet_up, (10, 10))
        self.photo_bullet_up.set_colorkey(BLACK)
        # DOWN
        self.photo_bullet_down = pygame.image.load("images/bullet_down.png").convert()
        self.photo_bullet_down = pygame.transform.scale(self.photo_bullet_down, (10, 10))
        self.photo_bullet_down.set_colorkey(BLACK)
        # RIGHT
        self.photo_bullet_right = pygame.image.load("images/bullet_right.png").convert()
        self.photo_bullet_right = pygame.transform.scale(self.photo_bullet_right, (10, 10))
        self.photo_bullet_right.set_colorkey(BLACK)
        # LEFT
        self.photo_bullet_left = pygame.image.load("images/bullet_left.png").convert()
        self.photo_bullet_left = pygame.transform.scale(self.photo_bullet_left, (10, 10))
        self.photo_bullet_left.set_colorkey(BLACK)

        self.photo_bullet = [self.photo_bullet_up, self.photo_bullet_down, self.photo_bullet_right,
                             self.photo_bullet_left]

        self.reward = 0
        self.running = True

    def step(self, action):
        if action == 5:
            self.player.shoot(self.my_bullet, self.photo_bullet)
        else:
            self.player.move(action)

        self.reward = 0

        if pygame.sprite.groupcollide(self.my_bullet, self.enemy_tanks, True, True):
            self.reward = 1
        if pygame.sprite.groupcollide(self.enemy_bullet, self.my_tank, True, True):
            self.reward = -1
            self.running = False
        pygame.sprite.groupcollide(self.my_bullet, self.all_wall, True, True)
        pygame.sprite.groupcollide(self.enemy_bullet, self.all_wall, True, True)

        if len(self.enemy_tanks) < 3:
            tank = choice(self.tanks)
            self.enemy_tanks.add(
                _enemy_tank.EnemyTank(tank, self.photo_enemy_tank, self.all_wall, self.enemy_bullet, self.photo_bullet))

        self.time -= 1
        if self.time < 0:
            self.running = False

        return self.reward, self.running

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

    def reset(self):
        # draw a map
        self.all_wall.empty()  # To clear a group of sprites
        for wall in [[300, 500], [225, 500], [150, 500], [25, 75], [75, 75]]:
            self.all_wall.add(_wall.Wall(wall, self.photo_wall))

        # player
        self.my_tank.empty()
        self.player = _player.MyTank([375, 625], self.photo_player, self.all_wall)
        self.my_tank.add(self.player)

        # enemy tanks
        self.enemy_tanks.empty()
        for tank in self.tanks:
            self.enemy_tanks.add(
                _enemy_tank.EnemyTank(tank, self.photo_enemy_tank, self.all_wall, self.enemy_bullet, self.photo_bullet))

        # Bullets
        self.my_bullet.empty()
        self.enemy_bullet.empty()

        # Play time
        self.time = FPS * 120

        self.running = True

        return self.running


def build_model(height, width, channels, actions):
    model = Sequential()
    model.add(Convolution2D(5200, (10, 10), activation='relu', input_shape=(height, width, channels)))
    model.add(Convolution2D(208, (5, 5), activation='relu'))
    model.add(Flatten())
    model.add(Dense(actions, activation='linear'))
    return model


def build_agent(model, actions):
    policy = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr='eps', value_max=1., value_min=.1, value_test=.2,
                                  nb_steps=10000)
    memory = SequentialMemory(limit=1000, window_length=3)
    dqn = DQNAgent(model=model, memory=memory, policy=policy,
                   enable_dueling_network=True, dueling_type='avg',
                   nb_actions=actions, nb_steps_warmup=1000
                   )
    return dqn


def main():
    env = TankEnv()
    actions = env.action_space.n
    height, width, channels = env.observation_space.shape
    print(height, width, channels)
    model = build_model(height, width, channels, actions)
    dqn = build_agent(model, actions)
    dqn.compile(Adam(lr=1e-4))
    dqn.fit(env, nb_steps=10000, visualize=False, verbose=2)

    scores = dqn.test(env, nb_episodes=10, visualize=True)
    print(np.mean(scores.history['episode_reward']))
    dqn.save_weights('SavedWeights/10k-Fast/dqn_weights.h5f')


if __name__ == '__main__':
    main()
    # Quit = False
    # action = 0
    # game = TankEnv()
    # while not Quit:
    #     running = game.reset()
    #     while running:
    #         game.clock.tick(FPS)
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 game.running = False
    #                 Quit = True
    #             elif event.type == pygame.KEYDOWN:
    #                 if event.key == pygame.K_UP:
    #                     action = 1
    #                 elif event.key == pygame.K_DOWN:
    #                     action = 2
    #                 elif event.key == pygame.K_RIGHT:
    #                     action = 3
    #                 elif event.key == pygame.K_LEFT:
    #                     action = 4
    #                 elif event.key == pygame.K_SPACE:
    #                     action = 5
    #         game.step(action)
    #         action = 0
    #         game.render()
    # pygame.quit()
