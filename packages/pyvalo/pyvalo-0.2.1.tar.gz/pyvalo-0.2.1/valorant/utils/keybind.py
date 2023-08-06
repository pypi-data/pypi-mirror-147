from dataclasses import dataclass, field
from pyautogui import typewrite


@dataclass
class General:
    primary_keybind: str = field(default="b")
    chat_keybind: str = field(default="enter")
    push_talk_party_keybind: str = field(default="u")
    push_talk_keybind: str = field(default="v")
    forward_keybind: str = field(default="w")
    backward_keybind: str = field(default="s")
    strafe_left_keybind: str = field(default="a")
    strafe_right_keybind: str = field(default="d")
    jump_keybind: str = field(default="space")
    crouch_keybind: str = field(default="ctrl")
    fire_keybind: str = field(default="leftclick")
    aim_keybind: str = field(default="rightclick")
    inspect_keybind: str = field(default="y")
    spray_keybind: str = field(default="t")
    ping_keybind: str = field(default="z")
    radio_command_menu_keybind: str = field(default=".")
    scoreboard_keybind: str = field(default="tab")
    map_keybind: str = field(default="capslock")
    armory_keybind: str = field(default="b")


@dataclass
class WeaponKeybind:
    primary_keybind: str = field(default="1")
    second_keybind: str = field(default="2")
    melee_keybind: str = field(default="3")
    spike_keybind: str = field(default="4")
    reload_keybind: str = field(default="r")
    drop_keybind: str = field(default="g")
    # get_keybind: str = field(default="f")


@dataclass
class AbilityKeybind:
    first_ability_keybind: str = field(default="q")  # q
    second_ability_keybind: str = field(default="e")  # e
    third_ability_keybind: str = field(default="c")  # c
    ultimate_keybind: str = field(default="x")  # x
    get_keybind: str = field(default="f")

    def first_ability(self):
        typewrite(self.first_ability_keybind)

    def second_ability(self):
        typewrite(self.first_ability_keybind)

    def third_ability(self):
        typewrite(self.third_ability_keybind)

    def ultimate_ability(self):
        typewrite(self.ultimate_keybind)
