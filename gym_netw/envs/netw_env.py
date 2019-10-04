import gym

import numpy as np
from gym import spaces
from socket import *

from gym_netw.envs.netw import Server

class NetwEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    
    def __init__(self, isDiscrete=True):
        self.server = Server (5050, 3)
        self.isDiscrete = isDiscrete
        
        if isDiscrete:
            self.action_space = spaces.Discrete (3);
        else:
            self.action_space = spaces.Box (low=-1, high=1, shape=(3,), dtype=np.float32)
            
        #self.observation_space = spaces.Tuple ((spaces.Discrete(1), spaces.Discrete(1), spaces.Discrete(1)))
        self.observation_space = spaces.Box (low=0, high=1, shape=(3,), dtype=np.float32)
        

    def step(self, action):
        
        # self.server._action (action)
        # print(action)
        # reward = self.server._reward ()
        # print(reward)
        # obs = self.server._obs ()
        # print(obs)
        # done = self.server._end ()
        # print(done)
        self.server._action (action, self.isDiscrete)
        obs, reward = self.server._communicate ()
        #reward = -reward
        # if reward != 0:
            # print(reward)
       
        done = self.server._end ()
        
        return obs, reward, done, {"None":1}

    def reset(self):
        #obs = np.zeros ((1,3))
        # obs = self.server._obs ()
        # print(obs)
        # dump = self.server._end ()
        
        obs, reward = self.server._communicate ()
        dump = self.server._end ()
        return obs

    def render(self):
        pass
