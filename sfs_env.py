import telemetry
from scripts import controls

class SFS_Env:
    def __init__(self):
        self.max_steps = 300
        self.last_state = None
        self.last_height = None
        self.episode_steps = 0

        self.actions = [
            "do_nothing",
            "throttle_up",
            "throttle_down",
            "rotate_left",
            "rotate_right",
            "stage"
        ]

    def reset(self):
        state = self.observe()
        self.episode_steps = 0
        self.last_state = state
        return state

    def step(self, action):
        # Increment step count and check for episode termination
        self.episode_steps += 1
        done = False
        
        # get state before action
        state_before = self.observe()

        # execute action
        controls.execute_action(action)

        # wait
        controls.wait_for_action_effect()

        # get state after action
        state_after = self.observe()

        # compute reward
        height_before = state_before[0]
        height_after = state_after[0]
        reward = height_after - height_before

        if reward < 1:
            reward -= 1

        if self.episode_steps >= self.max_steps:
            done = True

        self.last_state = state_after

        return state_after, reward, done

    def observe(self):
        return telemetry.get_state()