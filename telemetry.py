import time
import cv2
import mss
import numpy as np
import pytesseract
import re


SHOW_DEBUG_WINDOWS = False
OCR_INTERVAL = .03

GAME_REGION = {
    "left": 820,
    "top": 0,
    "width": 840,
    "height": 1050
}

VELOCITY_CROP = {
    "x1": 350,
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

THROTTLE_CROP = {
    "x1": 560,
    "y1": 920,
    "x2": 660,
    "y2": 960
}

TESS_CONFIG = r"--psm 7 -c tessedit_char_whitelist=0123456789.km/s%"


def extract_number(text):
    text = text.replace(",", ".")
    text = text.replace("O", "0")
    text = text.replace("o", "0")

    match = re.search(r"-?\d+\.?\d*", text)

    if match:
        return float(match.group())

    return None


def extract_height_meters(text):
    value = extract_number(text)

    if value is None:
        return None

    text = text.lower()

    if "km" in text:
        return value * 1000

    return value


def preprocess(crop):
    gray = cv2.cvtColor(crop, cv2.COLOR_BGRA2GRAY)

    gray = cv2.resize(
        gray,
        None,
        fx=3,
        fy=3,
        interpolation=cv2.INTER_CUBIC
    )

    _, gray = cv2.threshold(
        gray,
        180,
        255,
        cv2.THRESH_BINARY
    )

    return gray


def read_number(crop):
    processed = preprocess(crop)

    text = pytesseract.image_to_string(
        processed,
        lang="eng",
        config=TESS_CONFIG
    )

    value = extract_number(text)

    return value, text, processed


last_good_state = [13.5, 0.0, 50.0]


def get_state():
    global last_good_state

    with mss.mss() as sct:
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

    throttle_crop = img[
        THROTTLE_CROP["y1"]:THROTTLE_CROP["y2"],
        THROTTLE_CROP["x1"]:THROTTLE_CROP["x2"]
    ]

    velocity_value, velocity_text, velocity_processed = read_number(velocity_crop)
    _, height_text, height_processed = read_number(height_crop)
    throttle_value, throttle_text, throttle_processed = read_number(throttle_crop)

    height_value = extract_height_meters(height_text)

    if height_value is not None and velocity_value is not None and throttle_value is not None:
        state = [height_value, velocity_value, throttle_value]
        last_good_state = state.copy()
    else:
        state = last_good_state.copy()
        print("RAW OCR")
        print("height:", repr(height_text), "=>", height_value)
        print("velocity:", repr(velocity_text), "=>", velocity_value)
        print("throttle:", repr(throttle_text), "=>", throttle_value)
        print("STATE:", state)

    if SHOW_DEBUG_WINDOWS:
        cv2.imshow("Velocity Crop", velocity_crop)
        cv2.imshow("Height Crop", height_crop)
        cv2.imshow("Throttle Crop", throttle_crop)
        cv2.imshow("Velocity OCR", velocity_processed)
        cv2.imshow("Height OCR", height_processed)
        cv2.imshow("Throttle OCR", throttle_processed)
        cv2.waitKey(1)

    return state