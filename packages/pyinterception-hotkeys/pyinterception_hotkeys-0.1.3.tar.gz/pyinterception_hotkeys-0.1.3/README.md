# PyInterception Hotkeys

PyInterception Hotkeys는 PyInterception을 기반으로 한 파이썬 핫키 및 키보드 입력 라이브러리입니다. 이 라이브러리는 사용자 지정 핫키와 키보드 입력 이벤트를 처리하는 데 유용합니다.

## 설치

이 프로젝트를 설치하려면 다음 명령어를 사용하세요:

```sh
pip install pyinterception-hotkeys
```

## 사용법

다음은 PyInterception Hotkeys를 사용하는 예제 코드입니다:

```python
from pyInterception_hotkeys import keyboard, hotkey, KeyInputSource, Hotkey


def on_event(self: Hotkey):
    physical = "pressed" if keyboard.is_pressed(self.keys, mode=KeyInputSource.HARDWARE) else "released"
    software = "pressed" if keyboard.is_pressed("3", mode=KeyInputSource.SOFTWARE) else "released"

    print(f"Physical {self.keys} is {physical}")
    print(f"Software 3 is {software}")
    print()


def on_press(self):
    keyboard.press("3")
    on_event(self)


def on_release(self):
    keyboard.release("3")
    on_event(self)


# 핫키 등록 (예: Ctrl + Alt + H)
hotkey.add_hotkey(keys=set("1"), on_press=on_event, on_release=on_event)
hotkey.add_hotkey(keys=set("2"), on_press=on_press, on_release=on_release)

with keyboard as listener:
    listener.join()
```

이 예제에서 "1" 키와 "2" 키에 핫키를 설정하여 각 키가 눌렸을 때와 떼어졌을 때의 이벤트를 처리합니다.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE)를 참조하세요.