from sfs_env import SFS_Env
import random
import time

env = SFS_Env()
state = env.reset()

for i in range(50):
    action = random.choice(env.actions)

    state, reward, done = env.step(action)

    #print("step:", i, "action:", action, "state:", state, "reward:", reward, "done:", done)

    if done:
        break

    time.sleep(0.2)