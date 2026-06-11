import random
import pickle

class QAgent:
    def save(self, filename="q_table.pkl"):
        with open(filename, "wb") as file:
            pickle.dump(self.q_table, file)

    def load(self, filename="q_table.pkl"):
        try:
            with open(filename, "rb") as file:
                self.q_table = pickle.load(file)
        except FileNotFoundError:
            pass
            
    def __init__(self, actions):
        self.actions = actions
        self.memory = []
        self.q_table = {}

        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 0.2

    def ensure_state_exists(self, bucketed_state):
        if bucketed_state not in self.q_table:
            self.q_table[bucketed_state] = {a: 0.0 for a in self.actions}

    def choose_action(self, state):
        bucketed_state = self.bucket_state(state)
        self.ensure_state_exists(bucketed_state)

        if random.random() < self.epsilon:
            return random.choice(self.actions)

        return max(
            self.q_table[bucketed_state],
            key=self.q_table[bucketed_state].get
        )

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def bucket_state(self, state):
        height_bucket = int((state[0]) // 100)
        velocity_bucket = int((state[1]) // 10)
        throttle_bucket = int((state[2]) // 10)

        return (height_bucket, velocity_bucket, throttle_bucket)
    
    def update(self, state, action, reward, next_state):
        bucketed_state = self.bucket_state(state)
        bucketed_next_state = self.bucket_state(next_state)

        self.ensure_state_exists(bucketed_state)
        self.ensure_state_exists(bucketed_next_state)

        current_q = self.q_table[bucketed_state][action]
        max_next_q = max(self.q_table[bucketed_next_state].values())
        new_q = current_q + self.learning_rate * (
            reward +
            self.discount_factor * max_next_q -
            current_q
        )
        self.q_table[bucketed_state][action] = new_q