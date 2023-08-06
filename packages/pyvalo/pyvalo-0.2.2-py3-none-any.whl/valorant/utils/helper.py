import pyautogui
from valorant.utils.record import screenshot
from os import getcwd
from keyboard import wait
import warnings
import functools


def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)  # turn off filter
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning,
                      stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)  # reset filter
        return func(*args, **kwargs)

    return new_func


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


def check_position(name, base):
    try:
        if name == "buy_phase":
            return base.buy_phase_coor
        elif name == "check_enemy_score":
            return base.enemy_info_coor
        elif name == "check_own_score":
            return base.own_info_coor
        elif name == "time_left":
            return base.time_left_coor
        elif name == "check_money":
            return base.check_money_pos
        elif name == "tesseract":
            return base.tesseract_path
    except ValueError:
        pass


def scanning(name):
    def wrap(func):
        def scanner(*args, **kwargs):
            if isinstance(kwargs['config'], object) and kwargs['config'].__module__ == "valorant.base":
                path = getcwd() + "\\" + name + '.png'
                if 'config' in kwargs and func.__defaults__[0] is None:
                    img = screenshot(path, check_position(name, kwargs['config']))
                    kwargs['img'] = img
                else:
                    img = screenshot(path, check_position(name, args[0]))
                    kwargs['img'] = img

                return func(*args, **kwargs)
            else:
                raise Exception("Parameter must be config and the arguments need from valorant base class config")

        return scanner

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


def apply_config(base):
    def wrap(func):
        def inner(*args, **kwargs):
            # starting press buy button
            kwargs = {'base': base}
            func(*args, **kwargs)

        return inner

    return wrap
