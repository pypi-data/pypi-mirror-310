from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from functools import singledispatch
from types import MappingProxyType
from typing import Callable, Set

from interception import _keycodes, KeyStroke
from win32gui import GetForegroundWindow, FindWindow


class HotkeyEventType(Enum):
    PRESSED = 0
    RELEASED = 1


class HotkeyEvent:
    def __init__(self, callback=None):
        super().__init__()
        self._is_active = False
        self.callback = callback

    def execute(self, *args, **kwargs):
        if self.callback:
            self._is_active = True
            try:
                self.callback(*args, **kwargs)
            finally:
                self._is_active = False

    @property
    def is_active(self):
        return self._is_active


class Hotkey:
    """
    Hotkey 객체를 생성하는 클래스

    Attributes:
        keycodes (frozenset): 핫키에 사용할 키의 스캔 코드
    """

    def __init__(self, keys: Set[str], on_press: Callable = None, on_release: Callable = None, suppress: bool = True,
                 window_class: str = None):
        """
        Hotkey 객체를 생성하는 생성자

        :param keys: 핫키에 사용할 키 목록 (리스트로 처리)
        :param on_press: 키가 눌렸을 때 호출될 콜백 함수
        :param on_release: 키가 떼어졌을 때 호출될 콜백 함수
        :param suppress: True이면 시스템의 기본 동작을 억제 (기본값은 True)
        """
        self._enabled = True
        self._state = HotkeyEventType.RELEASED
        self.keys = frozenset(keys)
        self.keycodes = frozenset([_keycodes.get_key_information(key).scan_code for key in keys])

        self._events = MappingProxyType({
            HotkeyEventType.PRESSED: HotkeyEvent(callback=on_press),
            HotkeyEventType.RELEASED: HotkeyEvent(callback=on_release)
        })

        self._window_class = window_class

        self._suppress = suppress
        self._threadPool = ThreadPoolExecutor(max_workers=2)

    def _handle_event(self, event_type: HotkeyEventType, hwnd):
        """키가 눌러졌을 때 호출되는 메서드"""
        suppress = False
        if self._enabled and (not self._window_class or hwnd == FindWindow(self._window_class, None)):
            self._state = event_type

            event = self._events[event_type]
            suppress = self._suppress

            if not event.is_active:
                self._threadPool.submit(event.execute, self)

        return suppress

    def handle_press(self, hwnd):
        """키가 눌러졌을 때 호출되는 메서드"""
        return self._handle_event(HotkeyEventType.PRESSED, hwnd)

    def handle_release(self, hwnd):
        """키가 떼어졌을 때 호출되는 메서드"""
        return self._handle_event(HotkeyEventType.RELEASED, hwnd)

    def disable(self):
        self._enabled = False

    def enable(self):
        self._enabled = True

    def is_pressed(self):
        return self._state == HotkeyEventType.PRESSED

    def is_active(self, event_type: HotkeyEventType):
        return self._events[event_type].is_active


class HotkeyManager:
    """
    핫키 리스너 - 등록된 핫키를 감지하고 콜백 실행.
    """

    def __init__(self):
        self._hotkeys = {}

    @singledispatch
    def add_hotkey(self, hotkey: Hotkey):
        """
        핫키를 등록.
        """
        self._hotkeys[hotkey.keycodes] = hotkey

    @add_hotkey.register
    def add_hotkey(self, keys: set, on_press: Callable = None, on_release: Callable = None, suppress: bool = True,
                   window_class: str = None):
        """
        핫키를 등록.
        """
        hotkey = Hotkey(keys, on_press, on_release, suppress, window_class)
        self._hotkeys[hotkey.keycodes] = hotkey

    def remove_hotkey(self, keys: set):
        """
        핫키를 제거.
        """
        self._hotkeys.pop(frozenset(keys), None)

    def handle_key_event(self, stroke: KeyStroke, pressed_keycodes):
        """
        현재 눌린 키 상태와 매핑된 핫키를 확인하여 콜백 실행.
        """
        suppress = False
        hwnd = GetForegroundWindow()

        for keycodes, hotkey in self._hotkeys.items():
            if stroke.code in keycodes and all(key in pressed_keycodes for key in keycodes):  # 핫키 조건 충족
                suppress = suppress or hotkey.handle_press(hwnd)

            elif hotkey.is_pressed() and any(key not in pressed_keycodes for key in keycodes):  # 핫키 조건 해제
                suppress = suppress or hotkey.handle_release(hwnd)

        return suppress
