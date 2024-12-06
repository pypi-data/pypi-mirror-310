import random
import time
from functools import partial
from threading import Timer, Thread

from interception import Interception, KeyStroke, FilterKeyFlag, KeyFlag, _keycodes

from ._hotkey import HotkeyManager
from ._keyStateTracker import KeyStateTracker, KeyInputSource


class KeyboardListener(Thread):
    """
    키보드 입력을 관리하는 매니저.
    """

    def __init__(self, hotkey_manager: HotkeyManager = None):
        super().__init__()
        self.daemon = True

        self._running = True
        self._hotkey_manager = hotkey_manager
        self._state_tracker = KeyStateTracker()
        self.context = Interception()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def run(self):
        self.context.set_filter(self.context.is_keyboard, FilterKeyFlag.FILTER_KEY_ALL)

        while self._running and (device := self.context.await_input()):
            if device is not None:
                stroke = self.context.devices[device].receive()

                if not isinstance(stroke, KeyStroke):
                    continue

                if not self._key_event_handler(stroke):
                    self.context.send(device, stroke)

    def _key_event_handler(self, stroke: KeyStroke):
        keycode = stroke.code

        # 물리적 키 상태 업데이트
        self._state_tracker.update_physical_key(keycode, stroke.flags)

        # 핫키 리스너에 이벤트 전달
        return self._hotkey_manager.handle_key_event(stroke, self._state_tracker.get_all_keycodes(KeyInputSource.HARDWARE))

    def is_pressed(self, keys, mode: KeyInputSource = KeyInputSource.HARDWARE):
        """
        특정 키가 눌려 있는지 확인.
        """
        key_set = keys if isinstance(keys, (list, tuple, set)) else {keys}
        return self._state_tracker.is_pressed(key_set, mode)

    def _key_event(self, key, key_flag, delay, random_delay):
        """
        Simulate a key event.
        Args:
            key (keyboard.KeyCode | keyboard._key.py): Simulated key.
            delay (int): Delay time after function execution in milliseconds.
            random_delay (int): Randomly added delay time in milliseconds.
        """
        scan_code = _keycodes.get_key_information(key).scan_code

        stroke = KeyStroke(scan_code, key_flag)
        stroke.information = 999

        self._state_tracker.update_software_key(scan_code, stroke.flags)

        self.context.send(self.context.keyboard, stroke)

        milliseconds = (delay + random.randrange(0, random_delay)) / 1000
        time.sleep(milliseconds)

    def press(self, key, delay=30, random_delay=20):
        """
        Simulate a keydown event.
        Args:
            key (keyboard.KeyCode | keyboard._key.py): Simulated key.
            delay (int): Delay time after function execution in milliseconds.
            random_delay (int): Randomly added delay time in milliseconds.
        """
        self._key_event(key, KeyFlag.KEY_DOWN, delay, random_delay)

    def release(self, key, delay=30, random_delay=20):
        """
        Simulate a keyup event.
        Args:
            key (keyboard.KeyCode | keyboard._key.py): Simulated key.
            delay (int): Delay time after function execution in milliseconds.
            random_delay (int): Randomly added delay time in milliseconds.
        """
        if self.is_pressed(key, KeyInputSource.SOFTWARE):
            self._key_event(key, KeyFlag.KEY_UP, delay, random_delay)

    def tap(self, key, delay=30, random_delay=20, duration=50, random_duration=20):
        """
        Simulate a keydown and keyup event.
        Args:
            key (keyboard.KeyCode | keyboard._key.py): Simulated key.
            delay (int): Delay time after function execution in milliseconds.
            random_delay (int): Randomly added delay time in milliseconds.
            duration (int):
            random_duration (int):
        """
        bound_release = partial(self.release, key)

        if random_duration != 0:
            duration += random.randrange(0, random_duration)

        Timer(duration / 1000, bound_release).start()
        self.press(key, delay, random_delay)


hotkey = HotkeyManager()
keyboard = KeyboardListener(hotkey)
keyboard.start()
