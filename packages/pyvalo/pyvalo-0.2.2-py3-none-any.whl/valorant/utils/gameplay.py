import cv2
from valorant.utils.preprocessing import Image
from valorant.utils.helper import scanning, deprecated

image = Image()


@scanning(name="buy_phase")
def check_buy_phase(img=None, **kwargs):
    """
    Check buy phase is exists
    :return: boolean
    if True then it's in the buy phase
    if False then it's not in the buy phase, so you can't buy
    """
    text = process_score(img, 9, config=kwargs)
    text = text.split('\n')
    masked_image = image.masking_color(img, (0, 0, 234), (179, 9, 255), 1, 2)  # detect time upper than 15 seconds
    text = image.ocr(masked_image, config=kwargs).rstrip()
    text = text.split('\n')
    print(text)
    buy_text = ['pres', 'press', 'to', 'to buy', 'press [b] to buy', 'press [b] to guy', 'press [8] to buy', 'buy',
                'to', 'press [b] to buy', 'buy phase']
    for i in text:
        if i.lower() in buy_text:
            return True
    return False


@scanning(name="time_left")
def time_left(img=None, **kwargs):
    """
    Check the time is left how many minute or second
    :return: string [3 number]
    if the return 121, it's mean 1 minute 21 seconds or 1:21
    if the return 021, it;s mean 21 seconds or 0:21w
    """

    masked_image = image.masking_color(img, (0, 0, 252), (179, 3, 255), 1, 2)  # detect time upper than 15 seconds
    text = image.ocr(masked_image, digit_only=True, config=kwargs).rstrip()
    print(text)
    if text is not None and len(text) >= 3:
        return text

    masked_image = image.masking_color(img, (0, 0, 0), (179, 225, 255), 3, 4)  # detect red color on 15 seconds left
    text = image.ocr(masked_image, digit_only=True, config=kwargs).rstrip()
    if text is None:
        return "015"
    return text


@deprecated
def process_score(img, sensitivity, text=True, config=None):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img = image.detect_white(img, sensitivity)
    if text:
        value = image.ocr(img, config=config)
    else:
        value = image.ocr(img, digit_only=True, config=config).rstrip()
    return value


@scanning(name="check_enemy_score")
def enemy_score_info(img=None, **kwargs):
    """
    Check enemy score info
    :param img: default None
    :param kwargs: config only
    :return: int
    """
    masked_image = image.masking_color(img, (0, 0, 252), (179, 3, 255), 1, 2)  # detect time upper than 15 seconds
    text = image.ocr(masked_image, digit_only=True, config=kwargs).rstrip()
    if text is None:
        masked_image = image.masking_color(img, (0, 0, 252), (179, 3, 255), 1, 3)  # detect time upper than 15 seconds
        text = image.ocr(masked_image, digit_only=True, config=kwargs).rstrip()
    return text


@scanning(name="check_own_score")
def own_score_info(img=None, **kwargs):
    """
     Check own score info
    :param img: default None
    :param kwargs: config only
    :return: int
    """
    masked_image = image.masking_color(img, (0, 0, 252), (179, 3, 255), 1, 2)  # detect time upper than 15 seconds
    text = image.ocr(masked_image, digit_only=True, config=kwargs).rstrip()
    return text
