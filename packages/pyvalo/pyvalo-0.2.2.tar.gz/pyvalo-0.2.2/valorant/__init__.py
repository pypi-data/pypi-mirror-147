from .utils import agent, communication, gameplay, helper, keybind, market, preprocessing, record
from .base import ValorantBase
from . import version
import pyautogui


def config(**kwargs):
    """
    Set a config
    :param kwargs:
    tesseract = Your Tesseract.exe location full path. example: r"C:\Program Files\Tesseract-OCR\tesseract.exe",

    check_money_pos = Location of creds in buy weapon section. example: (250, 120, 110, 55),

    check_buy_phase = Location of buying phase text. example:(810, 140, 310, 140),

    enemy_score_info = Location of enemy score info. example:(750, 25, 100, 55),

    own_score_info = Location of own score info. example:(1050, 25, 100, 55),

    time_left_pos = Location of gameplay time. example: (900, 25, 100, 55),

    failsafe = User can interrupt keyboard without crash if it is True
    :return: ValorantBase
    """
    if 'config' in kwargs:
        return ValorantBase.config(**kwargs)
    else:
        # default value
        _tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        _check_money_pos = (250, 120, 110, 55)
        _check_buy_phase = (810, 140, 310, 140)
        _own_score_info = (750, 25, 100, 55)
        _enemy_score_info = (1050, 25, 100, 55)
        _time_left_pos = (900, 25, 100, 55)
        _failsafe = True

        if 'tesseract' not in kwargs:
            kwargs['tesseract'] = _tesseract

        if 'check_money_pos' not in kwargs:
            kwargs['check_money_pos'] = _check_money_pos

        if 'check_buy_phase' not in kwargs:
            kwargs['check_buy_phase'] = _check_buy_phase

        if 'enemy_score_info' not in kwargs:
            kwargs['enemy_score_info'] = _enemy_score_info

        if 'own_score_info' not in kwargs:
            kwargs['own_score_info'] = _own_score_info

        if 'time_left_pos' not in kwargs:
            kwargs['time_left_pos'] = _time_left_pos

        if 'failsafe' not in kwargs:
            kwargs['failsafe'] = _failsafe
            pyautogui.FAILSAFE = _failsafe

    return ValorantBase(**kwargs)


__version_info__ = version.VERSION
__version__ = version.VERSION_TEXT

__all__ = [
    'agent',
    'communication',
    "gameplay",
    'helper',
    "keybind",
    "market",
    "preprocessing",
    "record",
]
