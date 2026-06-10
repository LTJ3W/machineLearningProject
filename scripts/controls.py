import pydirectinput
import time

#Controls that are toggle based and only require a single key press
def ignition():
    pydirectinput.press('space')

def throttle_max():
    pydirectinput.press('z')

def throttle_kill():
    pydirectinput.press('x')

def toggle_res():
    pydirectinput.press('r')

def activate_stage():
    pydirectinput.press('enter')

#Controls that are hold based and require key pressing and holding down the key for the duration of the action
def rotate_left(duration):
    pydirectinput.keyDown('q')
    time.sleep(duration)
    pydirectinput.keyUp('q')

def rotate_right(duration):
    pydirectinput.keyDown('e')
    time.sleep(duration)
    pydirectinput.keyUp('e')

def throttle_up(duration):
    pydirectinput.keyDown('shift')
    time.sleep(duration)
    pydirectinput.keyUp('shift')

def throttle_down(duration):
    pydirectinput.keyDown('ctrl')
    time.sleep(duration)
    pydirectinput.keyUp('ctrl')

    #Movement controls for RES mode

def move_up_res(duration):
    pydirectinput.keyDown('w')
    time.sleep(duration)
    pydirectinput.keyUp('w')

def move_down_res(duration):
    pydirectinput.keyDown('s')
    time.sleep(duration)
    pydirectinput.keyUp('s')

def move_left_res(duration):
    pydirectinput.keyDown('a')
    time.sleep(duration)
    pydirectinput.keyUp('a')

def move_right_res(duration):
    pydirectinput.keyDown('d')
    time.sleep(duration)
    pydirectinput.keyUp('d')

#Action execution and timing functions
def execute_action(action, duration=0.15):
    if action == "do_nothing":
        time.sleep(duration)

    elif action == "throttle_up":
        throttle_up(duration)

    elif action == "throttle_down":
        throttle_down(duration)

    elif action == "rotate_left":
        rotate_left(duration)

    elif action == "rotate_right":
        rotate_right(duration)

    elif action == "stage":
        activate_stage()

    else:
        raise ValueError(f"Unknown action: {action}")

# Wait function to allow time for the action to take effect before observing the new state
def wait_for_action_effect(duration=0.25):
    time.sleep(duration)