import time
import cv2
import mss
import numpy as np
import pytesseract
import re

def extract_number(text):
    text = text.replace(",", ".")
    text = text.replace("O", "0")
    text = text.replace("o", "0")

    match = re.search(r"-?\d+\.?\d*", text)

    if match:
        return float(match.group())

    return None

def parse_height(text):
    return extract_number(text)


def parse_velocity(text):
    return extract_number(text)


def parse_throttle(text):
    lines = text.splitlines()

    for line in lines:
        if "%" in line:
            return extract_number(line)

    return extract_number(text)

# Manual capture region for the right side where SFS is visible
GAME_REGION = {
    "left": 820,
    "top": 0,
    "width": 840,
    "height": 1050
}

# Crop coordinates INSIDE the captured game image
# Format: y1:y2, x1:x2
TELEMETRY_CROP = {
    "x1": 400,
    "y1": 875,
    "x2": 840,
    "y2": 1025
}

VELOCITY_CROP = {
    "x1": 400,
    "y1": 900,
    "x2": 530,
    "y2": 1050
}

THROTTLE_CROP = {
    "x1": 520,
    "y1": 875,
    "x2": 750,
    "y2": 975
}

HEIGHT_CROP = {
    "x1": 700,
    "y1": 875,
    "x2": 840,
    "y2": 1050
}

with mss.mss() as sct:
    while True:
        last_time = time.time()

        # Capture the SFS region once
        screenshot = sct.grab(GAME_REGION)
        img = np.array(screenshot)

        # Crop telemetry from the captured image
        telemetry = img[
            TELEMETRY_CROP["y1"]:TELEMETRY_CROP["y2"],
            TELEMETRY_CROP["x1"]:TELEMETRY_CROP["x2"]
        ]

        # Crop velocity from the captured image
        velocity = img[
            VELOCITY_CROP["y1"]:VELOCITY_CROP["y2"],
            VELOCITY_CROP["x1"]:VELOCITY_CROP["x2"]
        ]

        # Crop throttle from the captured image
        throttle = img[
            THROTTLE_CROP["y1"]:THROTTLE_CROP["y2"],
            THROTTLE_CROP["x1"]:THROTTLE_CROP["x2"]
        ]

        # Crop height from the captured image
        height = img[
            HEIGHT_CROP["y1"]:HEIGHT_CROP["y2"],
            HEIGHT_CROP["x1"]:HEIGHT_CROP["x2"]
        ]

        # Show full capture and telemetry crop
        #cv2.imshow("SFS Capture", img)
        #cv2.imshow("Telemetry Crop", telemetry)
        cv2.imshow("Velocity Crop", velocity)
        cv2.imshow("Throttle Crop", throttle)
        #cv2.imshow("Height Crop", height)

        height_text = pytesseract.image_to_string(height, lang='eng')
        velocity_text = pytesseract.image_to_string(velocity, lang='eng')
        throttle_text = pytesseract.image_to_string(throttle, lang='eng')

        height_value = extract_number(height_text)
        velocity_value = extract_number(velocity_text)
        throttle_value = extract_number(throttle_text)

        state = [height_value, velocity_value, throttle_value]

        height_value = parse_height(height_text)
        velocity_value = parse_velocity(velocity_text)
        throttle_value = parse_throttle(throttle_text)

        if height_value is not None and velocity_value is not None and throttle_value is not None:
            state = [height_value, velocity_value, throttle_value]
            print(state)
        else:
            print("Bad OCR frame")
            print("height:", repr(height_text))
            print("velocity:", repr(velocity_text))
            print("throttle:", repr(throttle_text))

        #print(state)

        print("fps:", 1 / (time.time() - last_time))

        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break