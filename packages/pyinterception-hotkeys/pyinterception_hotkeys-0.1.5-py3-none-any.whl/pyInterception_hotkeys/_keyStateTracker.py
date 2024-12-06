from enum import Enum

from interception import KeyFlag, _keycodes


class KeyInputSource(Enum):
    HARDWARE = 1
    SOFTWARE = 2
    BOTH = 3


class KeyStateTracker:
    """
    물리적 및 소프트웨어 키 상태를 추적.
    """

    def __init__(self):
        self._physical_keycodes = set()
        self._software_keycodes = set()

    @staticmethod
    def _is_flag_pressed(flag: int):
        # KEY_E0, KEY_E1 to KEY_DOWN, KEY_UP
        return (flag % KeyFlag.KEY_E0) == KeyFlag.KEY_DOWN

    def update_physical_key(self, keycode, flag: int):
        is_pressed = self._is_flag_pressed(flag)

        if is_pressed:
            self._physical_keycodes.add(keycode)
        else:
            self._physical_keycodes.discard(keycode)

    def update_software_key(self, keycode, flag: int):
        is_pressed = self._is_flag_pressed(flag)
        if is_pressed:
            self._software_keycodes.add(keycode)
        else:
            self._software_keycodes.discard(keycode)

    def is_pressed(self, keys: set, mode):
        keycodes = [key if isinstance(key, int) else _keycodes.get_key_information(key).scan_code for key in keys]

        if mode == KeyInputSource.HARDWARE:
            return all(keycode in self._physical_keycodes for keycode in keycodes)
        elif mode == KeyInputSource.SOFTWARE:
            return all(keycode in self._software_keycodes for keycode in keycodes)
        elif mode == KeyInputSource.BOTH:
            return (all(keycode in self._physical_keycodes for keycode in keycodes)
                    or all(keycode in self._software_keycodes for keycode in keycodes))
        return False

    def get_all_keycodes(self, mode):
        if mode == KeyInputSource.HARDWARE:
            return self._physical_keycodes
        elif mode == KeyInputSource.SOFTWARE:
            return self._software_keycodes
        elif mode == KeyInputSource.BOTH:
            return self._physical_keycodes.union(self._software_keycodes)
        return set()
