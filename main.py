# main.py
from ui.main_window import MainWindow
from core.app_controller import AppController
from hotkeys.hotkey_listener import HotkeyListener
from config.settings import HOTKEY_COMBINATION

def main():
    main_window = MainWindow()
    controller = AppController(main_window=main_window)

    hotkey_listener = HotkeyListener(
        hotkey=HOTKEY_COMBINATION,
        callback=controller.handle_hotkey
    )
    hotkey_listener.start()

    main_window.mainloop()

if __name__ == "__main__":
    main()
