import pyautogui
from valorant.utils.record import screenshot
from os import getcwd
from keyboard import record, wait
from valorant.utils.agent import Abilities

def buy_tab():
    pyautogui.press('b')


def tab():
    pyautogui.press('tab')


def auto_buy_tab(func):
    def inner(*args, **kwargs):
        # starting press buy button
        pyautogui.press('b')
        value = func(*args, **kwargs)
        # starting press buy button to close
        pyautogui.press('b')
        return value

    return inner


def auto_screenshot(name, crop):
    def wrap(func):
        def inner(*args, **kwargs):
            if 'img' not in kwargs:
                path = getcwd() + "\\" + name
                img = screenshot(path, crop)
                kwargs = {'img': img}
            value = func(*args, **kwargs)
            return value

        return inner

    return wrap


def auto_chat_tab(func):
    def inner(*args, **kwargs):
        # starting press buy button
        pyautogui.press('enter')
        value = func(*args, **kwargs)
        # starting press buy button to close
        pyautogui.press('enter')
        pyautogui.press('enter')
        return value

    return inner


def shortcut(key: str, msg=None):
    def wrap(func):
        def inner(*args, **kwargs):
            # starting press buy button
            wait(key)
            if msg is not None:
                print(f"Message: {msg}")
            func(*args, **kwargs)

        return inner

    return wrap
