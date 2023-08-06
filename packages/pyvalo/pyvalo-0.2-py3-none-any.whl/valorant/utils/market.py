import os

import pyautogui
import re
from valorant.utils.preprocessing import Image
from valorant.utils.helper import auto_buy_tab, auto_screenshot
from valorant.config import MarketConfig

pyautogui.FAILSAFE = True
_config = MarketConfig()


class Shop:
    def __init__(self, config=_config):
        global _config
        self.image = Image()
        self.current_money = 800
        _config = config
        self.img = None
        self._weapons = {
            'eco': [0, (0, 0)],
            "stinger": [950, (703, 210)],
            "spectre": [1600, (676, 376)],
            "bucky": [850, (687, 543)],
            "judge": [1850, (677, 662)],
            "bulldog": [2050, (912, 216)],
            "guardian": [2250, (891, 360)],
            "phantom": [2900, (900, 522)],
            "vandal": [2900, (904, 670)],
            "marshal": [950, (1174, 200)],
            "operator": [4700, (1177, 355)],
            "ares": [1600, (1151, 539)],
            "odin": [3200, (1184, 658)],
            "classic": [0, (467, 200)],
            "shorty": [150, (506, 332)],
            "frenzy": [450, (482, 438)],
            "ghost": [500, (474, 552)],
            "sheriff": [800, (478, 675)],
            'no_shield': [0, (0, 0)],
            "heavy_shield": [1000, (1421, 597)],
            "light_shield": [400, (1429, 298)]
        }

    def __getitem__(self, key):
        return self._weapons.__getitem__(key)

    def __setitem__(self, key, value):
        return self._weapons.__setitem__(key, value)

    def __str__(self):
        return str(self._weapons)

    @property
    def weapons(self):
        return self._weapons

    @weapons.setter
    def weapons(self, primary):
        self._weapons = primary

    @auto_buy_tab
    @auto_screenshot("check_money.png", _config.money_coor)
    def check_money(self, img=None):
        """
        for checking your current money and next money
        use it when buy phase
        :param img: object image cv2.imread (optional)
        :param show: boolean (optional)
        :return: tuple (current money, next money)
        """
        text = self.image.ocr(img)
        if text is None or len(text) == 0:
            return 0
        split_text = text.split('\n')
        processed_test = list(filter(None, split_text))
        current_money = ''.join(processed_test[0].split(','))
        if not current_money.isdigit():
            current_money = re.findall(r'\b\d+\b', current_money)[0]
        # next_money = re.findall(r'\b\d+\b', processed_test[1])
        # if len(next_money) == 2 and len(next_money[0]) == 2:
        #     next_money = str(next_money[0][1]) + str(next_money[1])
        return int(current_money)

    @auto_buy_tab
    def buy_weapon(self, money=None, primary_weapon='eco', secondary_weapon='classic', shield='no_shield'):
        if money is None:
            money = self.check_money()

        wish_list = [primary_weapon, secondary_weapon, shield]
        for item in wish_list:
            if item in self._weapons:
                price, loc = self._weapons[item]
                if money >= price:
                    money -= price
                    pyautogui.click(loc)

    @staticmethod
    def drop_weapon(weapon="all"):
        """
        drop weapon
        :param weapon: 'all','primary','secondary';
        :return:
        """
        if weapon == "all":
            pyautogui.press("1")
            pyautogui.press("g")
            pyautogui.press("2")
            pyautogui.press("g")
        elif weapon == "primary":
            pyautogui.press("1")
            pyautogui.press("g")
        elif weapon == "secondary":
            pyautogui.press("2")
            pyautogui.press("g")
