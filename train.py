from sfs_env import SFS_Env
from agent import QAgent

env = SFS_Env()
agent = QAgent(env.actions)

agent.load()

state = env.reset()
total_reward = 0

for step in range(300):
    action = agent.choose_action(state)

    next_state, reward, done = env.step(action)

    agent.remember(state, action, reward, next_state, done)
    agent.update(state, action, reward, next_state)

    total_reward += reward

    print("step:", step)
    print("action:", action)
    print("reward:", round(reward, 2))
    print("q-table size:", len(agent.q_table))
    print()

    state = next_state

    if done:
        break

agent.save()

print("episode total reward:", round(total_reward, 2))