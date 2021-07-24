"""Font module

Select the best match font"""
from platform import system
from pathlib import Path
from typing import Optional

class FontSelector:
    """The font selection class

    The class try to match the best font via the following actions:
    1. check whether the font given is a path
    2. check the system font:
        1. if user's system is Liunx, try to get it from fclist
        2. if user's system is Windows, try to get it from system
    3. use one fallback font:
        1. fcmatch lang=zh-cn
        2. msyh.ttf or sumttf
    """
    def __init__(self, font: str = ""):
        self.desired_font = font
        self.best_font_path: Optional[Path] = None
        self.usefc = "linux" in system().lower()

    def _is_font_a_path(self):
        """check if it's a font path"""
        if self.best_font_path:
            return
        maybe_font_path = Path(self.desired_font)
        if maybe_font_path.exists() and maybe_font_path.is_file():
            self.best_font_path = maybe_font_path

    def __load_from_fc(self):
        from fclist import fclist
        for f in fclist(family=self.desired_font):
            self.best_font_path = Path(f.file)
            break

    def __load_from_windows(self):
        for fontpath in Path("C:\Windows\fonts").iterdir():
            if fontpath.is_file() and fontpath.name == self.desired_font:
                self.best_font_path = fontpath
                break

    def __load_fc_fallback(self):
        from fclist import fcmatch
        self.best_font_path = Path(fcmatch("sans-serif:lang=zh-cn").file)

    def __load_windows_fallback(self):
        for name in ["msyh", "simsun"]:
            for fontpath in Path("C:\Windows\fonts").iterdir():
                if name in fontpath.name.lower():
                    self.best_font_path = fontpath
                    break
            if self.best_font_path:
                break

    def _is_font_a_system_font_name(self):
        """check weather it is a system font name"""
        if self.best_font_path:
            return
        if self.usefc:
            self.__load_from_fc()
        else:
            self.__load_from_windows()

    def _is_font_no_match(self):
        """use the fallback font"""
        if self.best_font_path:
            return
        if self.usefc:
            self.__load_fc_fallback()
        else:
            self.__load_window_fallback()

    def select_the_best(self) -> Path:
        self._is_font_a_path()
        self._is_font_a_system_font_name()
        self._is_font_no_match()
        return self.best_font_path
