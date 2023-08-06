from valorant.utils.helper import auto_chat_tab
from pyautogui import typewrite, hotkey

@auto_chat_tab
def chat(text, party=False):
    if party:
        hotkey('shift', 'tab')
        typewrite('/party')
    typewrite(text)


@auto_chat_tab
def whisper(text, message_to=None):
    if message_to is not None:
        hotkey('shift', 'tab')
        typewrite(message_to)
        hotkey('tab')
    typewrite(text)
