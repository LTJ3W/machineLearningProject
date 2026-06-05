import pydirectinput
import time
from controls import ignition, throttle_max, throttle_kill, rotate_left, rotate_right, activate_stage

print("Click into Spaceflight Simulator. Test starts in 5 seconds.")
time.sleep(5)

print("Testing ignition...")
ignition()
time.sleep(2)

print("Testing stage activation...")
activate_stage()
time.sleep(2)

print("Testing throttle max...")
throttle_max()
time.sleep(2)

print("Testing rotate left...")
rotate_left(0.3)
time.sleep(2)

print("Testing rotate right...")
rotate_right(0.3)
time.sleep(2)

print("Testing throttle kill...")
throttle_kill()

print("Test complete.")