# # hotkeys/hotkey_listener.py
# from pynput import keyboard
# import threading
#
# class HotkeyListener:
#     def __init__(self, hotkey, callback):
#         self.hotkey = hotkey
#         self.callback = callback
#         self.listener = None
#
#     def start(self):
#         combo_parts = []
#         for key in self.hotkey:
#             if key.lower() in ('ctrl', 'shift', 'alt', 'cmd'):
#                 combo_parts.append(f'<{key.lower()}>')
#             else:
#                 combo_parts.append(key.lower())
#         hotkey_combination = '+'.join(combo_parts)
#
#         def on_activate():
#             threading.Thread(target=self.callback, daemon=True).start()
#
#         self.listener = keyboard.GlobalHotKeys({
#             hotkey_combination: on_activate
#         })
#         self.listener.start()


# hotkeys/hotkey_listener.py
from pynput import keyboard
import threading


MODIFIER_GROUPS = {
    'ctrl': {keyboard.Key.ctrl_l, keyboard.Key.ctrl_r},
    'shift': {keyboard.Key.shift_l, keyboard.Key.shift_r},
    'alt': {keyboard.Key.alt_l, keyboard.Key.alt_r},
    'cmd': {keyboard.Key.cmd_l, keyboard.Key.cmd_r},
}


class HotkeyListener:
    def __init__(self, hotkey, callback):
        self.callback = callback

        self.required_modifiers = []
        self.main_vk = None

        for key in hotkey:
            k = key.lower()
            if k in MODIFIER_GROUPS:
                self.required_modifiers.append(MODIFIER_GROUPS[k])
            else:
                # VK code for physical key, independent of layout
                self.main_vk = ord(k.upper())

        if self.main_vk is None:
            raise ValueError("Hotkey must contain a non-modifier key")

        self.pressed_keys = set()
        self.listener = None

    def start(self):
        def on_press(key):
            self.pressed_keys.add(key)

            if not isinstance(key, keyboard.KeyCode):
                return

            if key.vk != self.main_vk:
                return

            for group in self.required_modifiers:
                if not any(k in self.pressed_keys for k in group):
                    return

            threading.Thread(
                target=self.callback,
                daemon=True
            ).start()

        def on_release(key):
            self.pressed_keys.discard(key)

        self.listener = keyboard.Listener(
            on_press=on_press,
            on_release=on_release
        )
        self.listener.start()
