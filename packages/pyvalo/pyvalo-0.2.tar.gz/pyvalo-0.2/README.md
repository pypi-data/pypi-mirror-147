
# Pyvalo
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)

A valorant helper library to create your own assistant bot & strategy.



I'm not responsible if your account get ban but so far it's still safe to use.


## Requirements

- Python 3.9
- Tesseract Download https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.1.20220118.exe
https://github.com/UB-Mannheim/tesseract/wiki
- 1920 * 1080 Resolution, if your resolution different. Please change the value of default config to your config in config.ini 
## Features

- Buying Phase Validation
- Purchase Weapon and Shield
- Score Info
- Time Left Info
- Money Checker In-Game
- Drop Weapon
- Communication Chat
- Configuration
- Shortcut and Keybind
- Agents ability



## Installation

Install my-project with npm

```bash
  pip install pyvalo
```
    
# Usage/Examples

## Modify Existing weapon
Change this if valorant make any changes or your different resolution screen.
```python
from valorant import market


"""
[price, (x, y)]
x,y mean coordinate
[3000, (904, 670)]
"""
#modify price and coordinate
shop = market.Shop()
shop['vandal']=[3000, (904, 670)]
print(shop['vandal'])

#add new weapon
shop['new weapon']=[3100, (904, 670)]
print(shop['new weapon'])
```

## Agent Abilities and Keybind
Create agent combo shortcut using custom or default keybind and automatically return all information
```python
from valorant.utils.agent import Agent

if __name__ == '__main__':
    agent = Agent(first_ability_keybind="m")
    print(agent) #Agent(first_ability_keybind='m', second_ability_keybind='e', third_ability_keybind='c', ultimate_keybind='x', get_keybind='f', first_ability=0, second_ability=0, third_ability=0, ultimate_ability=1)
    agent.use_first_ability()
    agent.use_second_ability()
    agent.use_ultimate_ability()
```


## Chamber Combo
Create agent combo shortcut using custom or default keybind and automatically return all information
```python
from valorant.utils.helper import shortcut
from valorant.utils.agent import Chamber

if __name__ == '__main__':
    #chamber = Chamber()  # default keybind
    chamber = Chamber(first_ability_keybind="e", get_keybind="f") #custom keybind

    @shortcut("capslock", "Capslock Detected")
    def chambers_fake_tp():
        chamber.fake_tp()
        print(chamber)
        #Chamber(first_ability_keybind='e', second_ability_keybind='e', third_ability_keybind='c', ultimate_keybind='x', get_keybind='f', first_ability=0, second_ability=0, third_ability=0, ultimate_ability=1, fake_tp_keybind='ef')

    chambers_fake_tp()

    # access information of chamber first ability
    print(chamber.first_ability)
```

## Complete
Buy Assistant Bot, use it when you are afk for a moment (free customize)
```python
from valorant import market
from valorant.utils.gameplay import check_buy_phase
import time

shop = market.Shop()

while True:
    data = check_buy_phase()
    print(data)
    if data:
        current_money = shop.check_money()
        print("Current Money: ", str(current_money))
        # this is my buying strategy that mostly I use repeatedly
        primary = "vandal"
        secondary = "classic"
        shield = "heavy_shields"
        if 2000 <= current_money <= 2500:
            primary = "spectre"
        elif 2000 > current_money >= 1500:
            primary="marshal"
        elif 1400 <= current_money <= 2000:
            primary="marshal"
            shield = "light_shields"

        shop.buy_weapon(money=current_money, primary_weapon=primary, secondary_weapon=secondary,
                        shield=shield)
        shop.drop_weapon(weapon="all")
        print("Buy and drop weapon success")
    time.sleep(10)

```


## Support

For support, Join my discord https://discord.gg/HZJZAVAZdr


## Contributing

Contributions are always welcome!

See `contributing.md` for ways to get started.

Please adhere to this project's `code of conduct`.

