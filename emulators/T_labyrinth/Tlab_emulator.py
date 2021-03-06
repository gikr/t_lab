from ..env_T_2 import make_game, T_lab_observation, T_lab_actions, print_obs

from ..environment import BaseEnvironment

import numpy as np
import operator

def convert_obs(obs):
    obs, info = obs
    keys = sorted(info.keys())
    state = np.stack([info[k] for k in keys])
    return state.astype(np.uint8)

class TLabyrinthEmulator(BaseEnvironment):
    def __init__(self, emulator_id, game, random_seed=3,
                 random_start=True, single_life_episodes=False,
                 history_window=1, visualize=False, verbose=0, **unknown):
        self.randomness = True
        self.reward_location = np.random.choice([0,1]) #0 if np.random.rand() < 0.5 else 1
        self.visualize = visualize
        self.legal_actions = [0, 1, 2, 3] #['up', 'left', 'right', 'noop']
        #print(self.legal_actions)
        self.noop = 'pass'
        self.id = emulator_id
        self.length_int = [9,9]


        self.game, self.resultinig_length = make_game(False, self.reward_location, self.length_int)
        obs_t, r_t, discount_t = self.game.its_showtime()
        obs_t = convert_obs(obs_t)
        self.observation_shape = obs_t.shape


    def reset(self):
        """Starts a new episode and returns its initial state"""
        self.reward_location = np.random.choice([0,1]) #0 if np.random.rand() < 0.5 else 1
        #print("i don't knoooooow!", self.length_int)
        self.game, self.resultinig_length = make_game(False, self.reward_location, self.length_int)
        obs_t, r_t, discount_t = self.game.its_showtime()
        obs = convert_obs(obs_t)
        
        return obs, self.resultinig_length

    def next(self, action):

        """
        Performs the given action.
        Returns the next state, reward, and terminal signal
        """
        act = [i for i, x in enumerate(action) if x]
        if not self.game.game_over:
            obs, reward, discount = self.game.play(act[0])
            if self.visualize:
                act_names = ['up', 'left', 'right', 'noop']
                print('action={}, r={}, is_done={}'.format(act_names[act[0]], reward, discount!=1.0))
                print_obs(obs)
        termination = 1-discount

        return convert_obs(obs), reward, termination, self.resultinig_length


    def set_length(self, length_interval):
        #print('it works', length_interval)
        self.length_int = length_interval
        return self.resultinig_length


    def get_legal_actions(self):
        #self.legal_actions = T_lab_actions().shape
        return self.legal_actions

    def get_noop(self):
        #self.noop = 'pass'
        return self.noop

    def on_new_frame(self, frame):
        pass

    def close(self):
        pass
