# -*- coding: UTF-8 -*-
import gym
from RL_brain.deep_q_learning import DeepQNetwork
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def run_Mountain_Car(env, RL):
    total_steps = 0

    for i_episode in range(120):

        observation = env.reset()
        ep_r = 0
        while True:
            env.render()

            action = RL.choose_action(observation)

            observation_, reward, done, info = env.step(action)

            position, velocity = observation_

            # 车开得越高 reward 越大
            reward = abs(position - (-0.5))

            RL.store_transition(observation, action, reward, observation_)

            if total_steps > 1000:
                RL.learn()

            ep_r += reward
            if done:
                print('episode: ', i_episode,
                      'ep_r: ', round(ep_r, 2),
                      ' epsilon: ', round(RL.epsilon, 2))
                break

            observation = observation_
            total_steps += 1

if __name__ == "__main__":
    env = gym.make('MountainCar-v0')
    env = env.unwrapped

    print(env.action_space)
    print(env.observation_space)
    print(env.observation_space.high)
    print(env.observation_space.low)

    RL = DeepQNetwork(n_actions=3, n_features=2, learning_rate=0.001, e_greedy=0.9,
                      replace_target_iter=300, memory_size=3000,
                      e_greedy_increment=0.0001, )
    run_Mountain_Car(env, RL)
    RL.plot_cost()  # 观看神经网络的误差曲线