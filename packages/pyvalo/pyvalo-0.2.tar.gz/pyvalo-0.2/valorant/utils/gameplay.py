import cv2
from valorant.utils.preprocessing import Image
from valorant.utils.helper import auto_screenshot
from valorant.config import GameplayConfig

_config = GameplayConfig()
image = Image()


@auto_screenshot("buy_phase.png", _config.buy_phase_coor)
def check_buy_phase(img=None):
    """
    Check buy phase is exists
    :return: boolean
    if True then it's in the buy phase
    if False then it's not in the buy phase, so you can't buy
    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img = image.detect_white(img, 9)
    text = image.ocr(img)
    text = text.split('\n')
    buy_text = ['pres', 'press', 'to', 'to buy', 'press [b] to buy', 'press [b] to guy', 'press [8] to buy', 'buy',
                'to']
    for i in text:
        if i.lower() in buy_text:
            return True
    return False


@auto_screenshot("time_left.png", _config.time_left_coor)
def time_left(img=None):
    """
    Check the time is left how many minute or second
    :return: string [3 number]
    if the return 121, it's mean 1 minute 21 seconds or 1:21
    if the return 021, it;s mean 21 seconds or 0:21
    """
    cvt_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cvt_img = image.detect_white(cvt_img, 3)
    text = image.ocr(cvt_img).rstrip()
    if text is not None and len(text) >= 3:
        return text

    print("Red Time below 15 seconds")
    text = image.ocr(img).rstrip()
    if text is None:
        return "015"
    return text


def process_score(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img = image.detect_white(img, 3)
    score = image.ocr(img, digit_only=True).rstrip()
    return score


@auto_screenshot("check_enemy_score.png", _config.enemy_info_coor)
def enemy_score_info(img=None):
    return process_score(img)


@auto_screenshot("check_own_score.png", _config.own_info_coor)
def own_score_info(img=None):
    return process_score(img)
