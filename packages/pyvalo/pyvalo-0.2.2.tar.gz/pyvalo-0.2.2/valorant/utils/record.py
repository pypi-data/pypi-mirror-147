import cv2
import pyautogui
import os


def screenshot(path, crop=None, read=True):
    if crop is not None:
        pyautogui.screenshot(path, region=crop)
    else:
        pyautogui.screenshot(path)
    if read:
        image = cv2.imread(path, 1)
        os.remove(path)
        return image
    return None


def recording(path):
    pass
