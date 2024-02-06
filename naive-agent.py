import random
from environment.environment import Action, Environment

class NaiveAgent:

    def choose_action(self):
        # return a randomly chosen action
        random_number = random.randint(0,5)
        return Action(random_number)
    def run(self):
        env = Environment(0.2, True)
        cumulative_reward = 0
        percept = env.init(0.2, True)
        while not percept.done:
            env.visualize()
            print('Percept:', percept)
            action = self.choose_action()
            print()
            print('Action:', action)
            print()
            percept = env.step(action)
            cumulative_reward += percept.reward
        env.visualize()
        print('Percept:', percept)
        print('Cumulative reward:', cumulative_reward)
