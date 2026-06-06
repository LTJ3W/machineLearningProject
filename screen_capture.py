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




GAME_REGION = {
    "left": 820,
    "top": 0,
    "width": 840,
    "height": 1050
}

VELOCITY_CROP = {
    "x1": 400,
    "y1": 970,
    "x2": 530,
    "y2": 1000
}

HEIGHT_CROP = {
    "x1": 700,
    "y1": 970,
    "x2": 840,
    "y2": 1000
}

last_good_state = [13.5, 0.0, 50.0]
throttle_value = 50.0

with mss.mss() as sct:
    while True:
        last_time = time.time()

        screenshot = sct.grab(GAME_REGION)
        img = np.array(screenshot)

        velocity_crop = img[
            VELOCITY_CROP["y1"]:VELOCITY_CROP["y2"],
            VELOCITY_CROP["x1"]:VELOCITY_CROP["x2"]
        ]

        height_crop = img[
            HEIGHT_CROP["y1"]:HEIGHT_CROP["y2"],
            HEIGHT_CROP["x1"]:HEIGHT_CROP["x2"]
        ]

        cv2.imshow("Velocity Crop", velocity_crop)
        cv2.imshow("Height Crop", height_crop)

        height_text = pytesseract.image_to_string(
            height_crop,
            config=r'--psm 7'
        )

        velocity_text = pytesseract.image_to_string(
            velocity_crop,
            config=r'--psm 7'
        )

        height_value = extract_number(height_text)
        velocity_value = extract_number(velocity_text)

        if height_value is not None and velocity_value is not None:
            state = [height_value, velocity_value, throttle_value]
            last_good_state = state
        else:
            state = last_good_state
            print("Bad OCR frame")
            print("height:", repr(height_text))
            print("velocity:", repr(velocity_text))

        print("STATE:", state)
        print("fps:", 1 / (time.time() - last_time))

        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break