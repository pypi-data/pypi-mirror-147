from dataclasses import dataclass, field
from valorant.utils.keybind import AbilityKeybind
from pyautogui import typewrite


@dataclass
class Abilities:
    first_ability: int = field(default=1)
    second_ability: int = field(default=0)
    third_ability: int = field(default=0)
    ultimate_ability: int = field(default=1)

    def increment_first_ability(self, n=1):
        self.first_ability += n

    def decrease_first_ability(self, n=1):
        self.first_ability -= n
        if self.first_ability < 0:
            self.first_ability = 1
            print("First Ability set to default value (1)")


@dataclass
class Info:
    max_first_ability: int = field(default=1)
    max_second_ability: int = field(default=1)
    max_third_ability: int = field(default=1)
    max_ultimate_ability: int = field(default=1)

    first_ability_cooldown: int = field(default=1)
    second_ability_cooldown: int = field(default=1)
    third_ability_cooldown: int = field(default=1)
    ultimate_ability_cooldown: int = field(default=-1)

    def chamber(self):
        self.max_first_ability = 2
        self.max_second_ability = 8
        self.max_third_ability = 1
        self.max_ultimate_ability = 1

        self.first_ability_cooldown = -1
        self.second_ability_cooldown = -1
        self.third_ability_cooldown = 20
        self.ultimate_ability_cooldown = -1

    def sova(self):
        self.max_first_ability = 1
        self.max_second_ability = 2
        self.max_third_ability = 1
        self.max_ultimate_ability = 1

        self.first_ability_cooldown = -1
        self.second_ability_cooldown = -1
        self.third_ability_cooldown = 40
        self.ultimate_ability_cooldown = -1


@dataclass
class Agent(Abilities, AbilityKeybind):

    def use_first_ability(self):
        typewrite(self.first_ability_keybind)
        self.decrease_first_ability()

    def use_second_ability(self):
        typewrite(self.second_ability_keybind)
        self.decrease_first_ability()

    def use_third_ability(self):
        typewrite(self.third_ability_keybind)
        self.decrease_first_ability()

    def use_ultimate_ability(self):
        typewrite(self.ultimate_keybind)
        self.decrease_first_ability()


@dataclass
class Chamber(Agent):
    fake_tp_keybind: str = field(default="".join([Agent.first_ability_keybind, Agent.get_keybind]))

    def __post_init__(self):
        self.fake_tp_keybind = "".join([self.first_ability_keybind, self.get_keybind])

    def fake_tp(self):
        typewrite(self.fake_tp_keybind)
        self.decrease_first_ability()


# @dataclass
# class Omen(Abilities):
#     fake_tp_keybind: str = field(default="spacerightclick")
#     fake_ultimate_keybind: str = field(default="".join([AbilityKeybind.ultimate_keybind, AbilityKeybind.ultimate_keybind]))
#
#     def fake_tp(self):
#         typewrite(self.fake_tp_keybind)
#         self.decrease_first_ability()
#
#     def fake_ultimate(self, delay=5):
#         typewrite(self.fake_ultimate_keybind)
#         # self.decrease_first_ability()


if __name__ == '__main__':
    print('run')
    a1 = Abilities(1, 2, 3, 4)
    a1.increment_first_ability()
    a1.increment_first_ability()
    a1.increment_first_ability()
    a1.decrease_first_ability(15)
    print(a1)
