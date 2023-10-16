import pygame
from gym.spaces import Box, Discrete, Dict
import gym
from random import choice

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, ConvLSTM2D, Convolution2D, Flatten
from tensorflow.keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.memory import SequentialMemory
from rl.policy import BoltzmannQPolicy, LinearAnnealedPolicy, EpsGreedyQPolicy

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
        self.action_space = Discrete(6)
        # self.observation_space = Dict({"my_position": Box(low=np.array([0, 0]), high=np.array([WIDTH, HEIGHT])),
        #                                "enemy_positions": Box(low=np.array([0, 0]), high=np.array([WIDTH, HEIGHT])),
        #                                "wall_positions": Box(low=np.array([0, 0]), high=np.array([WIDTH, HEIGHT])),
        #                                "my_bullet": Box(low=np.array([0, 0]), high=np.array([WIDTH, HEIGHT])),
        #                                "enemy_bullet": Box(low=np.array([0, 0]), high=np.array([WIDTH, HEIGHT]))})
        self.observation_space = Box(low=0, high=255, shape=(WIDTH, HEIGHT, 3))

        # Pygame init
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Танчики")
        self.clock = pygame.time.Clock()

        # Play time (120 sec)
        self.time = FPS * 60

        # Walls init
        self.all_wall = pygame.sprite.Group()

        # Player's bullets init
        self.my_bullet = pygame.sprite.Group()

        # Enemies' bullets init
        self.enemy_bullet = pygame.sprite.Group()
        self.tanks = [[25, 25], [425, 25], [775, 25], [25, 325], [775, 325], [25, 625], [425, 625], [775, 625]]

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
        self.done = False

        ####################################################################
        self.screen_data = pygame.surfarray.array3d(self.screen)
        ####################################################################

    def step(self, action):
        if action == 5 and len(self.my_bullet) == 0:
            self.player.shoot(self.my_bullet, self.photo_bullet)
        else:
            self.player.move(action)

        if pygame.sprite.groupcollide(self.my_bullet, self.enemy_tanks, True, True):
            self.reward = 30
        elif pygame.sprite.groupcollide(self.enemy_bullet, self.my_tank, True, True):
            self.reward = -50
            self.done = True
        elif pygame.sprite.groupcollide(self.my_bullet, self.all_wall, True, True):
            self.reward = 1
        else:
            self.reward = -0.01
        pygame.sprite.groupcollide(self.enemy_bullet, self.all_wall, True, True)

        if len(self.enemy_tanks) < 8:
            tank = choice(self.tanks)
            self.enemy_tanks.add(
                _enemy_tank.EnemyTank(tank, self.photo_enemy_tank, self.all_wall, self.enemy_bullet, self.photo_bullet))

        self.time -= 1
        if self.time < 0:
            self.done = True
        if self.time % FPS == 0:
            print(self.time/FPS)
        # observation = self.get_obs()

        return self.screen_data, self.reward, self.done, {"info": "ok"}

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

        self.screen_data = pygame.surfarray.array3d(self.screen)
        pygame.display.flip()

    def reset(self):
        # draw a map
        self.all_wall.empty()  # To clear a group of sprites
        for wall in [[175, 25], [275, 25], [525, 25], [575, 25], [625, 25], [125, 75], [275, 75], [475, 75], [575, 75],
                     [675, 25], [725, 75], [75, 125], [125, 125], [175, 125], [225, 125], [275, 125], [325, 125],
                     [425, 125], [475, 125], [525, 125], [575, 125], [675, 125], [25, 175], [75, 175], [125, 175],
                     [575, 175], [625, 175], [675, 175], [725, 175], [775, 175], [25, 225], [75, 225], [175, 225],
                     [225, 225], [325, 225], [375, 225], [425, 225], [525, 225], [775, 225], [175, 275], [175, 275],
                     [325, 275], [375, 275], [475, 275], [525, 275], [575, 275], [625, 275], [725, 275], [225, 325],
                     [275, 325], [325, 325], [525, 325], [725, 325], [25, 375], [125, 375], [175, 375], [475, 375],
                     [525, 375], [625, 375], [675, 375], [775, 375], [125, 425], [175, 425], [225, 425], [325, 425],
                     [375, 425], [425, 425], [475, 425], [525, 425], [625, 425], [675, 425], [725, 425], [775, 425],
                     [25, 475], [75, 475], [175, 475], [325, 475], [625, 475], [675, 475], [75, 525], [175, 525],
                     [225, 525], [275, 525], [375, 525], [425, 525], [525, 525], [575, 525], [675, 525], [775, 525],
                     [125, 575], [225, 575], [325, 575], [525, 575], [625, 575], [675, 575], [725, 575], [75, 625],
                     [175, 625], [225, 625], [325, 625], [525, 625], [575, 625], [725, 625]]:
            self.all_wall.add(_wall.Wall(wall, self.photo_wall))

        # player
        self.my_tank.empty()
        self.player = _player.MyTank([425, 325], self.photo_player, self.all_wall)
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

        self.done = False
        # my_coord, my_bullet, enemy_coord, enemy_bullet, wall_coord = self.get_obs()
        #
        # return my_coord, my_bullet, enemy_coord, enemy_bullet, wall_coord
        # observation = self.get_obs()
        self.screen_data = pygame.surfarray.array3d(self.screen)
        return self.screen_data

    # def get_obs(self):
    #     observation = []
    #     for i in self.player.rect.center:
    #         observation.append(i)
    #
    #     for tank in self.enemy_tanks:
    #         for i in tank.rect.center:
    #             observation.append(i)
    #
    #     for wall in self.all_wall:
    #         for i in wall.rect.center:
    #             observation.append(i)
    #
    #     if len(self.all_wall) < 103:
    #         for i in range(103 - len(self.all_wall)):
    #             observation.append(-1)
    #             observation.append(-1)
    #
    #     for bullet in self.my_bullet:
    #         for i in bullet.rect.center:
    #             observation.append(i)
    #
    #     if len(self.my_bullet) < 1:
    #         for i in range(1 - len(self.my_bullet)):
    #             observation.append(-1)
    #             observation.append(-1)
    #
    #     for bullet in self.enemy_bullet:
    #         for i in bullet.rect.center:
    #             observation.append(i)
    #
    #     if len(self.enemy_bullet) < 16:
    #         for i in range(16 - len(self.enemy_bullet)):
    #             observation.append(-1)
    #             observation.append(-1)
    #
    #     observation = np.asarray(observation)
    #     print(observation)
    #     print(observation.shape)
    #     return observation
    #
    #     my_coord = self.player.rect.center
    #
    #     enemy_coord = []
    #     for tank in self.enemy_tanks:
    #         enemy_coord.append(tank.rect.center)
    #
    #     wall_coord = []
    #     for wall in self.all_wall:
    #         wall_coord.append(wall.rect.center)
    #
    #     my_bullet = []
    #     for bullet in self.my_bullet:
    #         my_bullet.append(bullet.rect.center)
    #
    #     enemy_bullet = []
    #     for bullet in self.enemy_bullet:
    #         enemy_bullet.append(bullet.rect.center)
    #
    #     observation = np.array([my_coord, my_bullet, enemy_coord, enemy_bullet, wall_coord])
    #     print(observation)
    #     return observation


def build_model(width, height, channels, actions):
    model = Sequential()
    model.add(ConvLSTM2D(32, (15, 15), strides=(3, 3), activation='relu', input_shape=(3, width, height, channels)))
    model.add(Convolution2D(16, (5, 5), strides=(3, 3), activation='relu'))
    model.add(Flatten())
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(actions, activation='linear'))
    return model


def build_agent(model, actions):
    model.summary()
    policy = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr='eps', value_max=1., value_min=.1, value_test=.2,
                                  nb_steps=10000)
    memory = SequentialMemory(limit=1000000, window_length=3)
    return DQNAgent(
        model=model,
        memory=memory,
        policy=policy,
        enable_dueling_network=True,
        dueling_type='avg',
        nb_actions=actions,
        nb_steps_warmup=1000,
        batch_size=2,
    )


def main():
    env = TankEnv()
    actions = env.action_space.n
    width, height, channels = env.observation_space.shape
    model = build_model(width, height, channels, actions)
    dqn = build_agent(model, actions)
    dqn.compile(Adam(lr=1e-4))
    dqn.fit(env, nb_steps=100000, visualize=True, verbose=2)
    dqn.save_weights('SavedWeights/10k-Fast/dqn_weights.h5f', overwrite=True)
    # dqn.load_weights('SavedWeights/10k-Fast/dqn_weights.h5f')
    # scores = dqn.test(env, nb_episodes=10, visualize=True)
    # print(np.mean(scores.history['episode_reward']))


if __name__ == '__main__':
    main()
