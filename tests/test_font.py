from weathercn.font import FontSelector
from pathlib import Path
import pytest

class TestFontSelector:
    def test_is_font_a_path(self):
        path = "/home/ssfdust/NextCloud/备份/Fonts/FZLanTYK_Cu.ttf"
        selector = FontSelector(path)
        assert selector.select_the_best() == Path(path)

    @pytest.mark.parametrize("name", ["WenQuanYi Zen Hei","文泉驛正黑","文泉驿正黑"])
    def test_is_system_font(self, name: str):
        selector = FontSelector(name)
        path = "/usr/share/fonts/wenquanyi/wqy-zenhei/wqy-zenhei.ttc"
        assert selector.select_the_best() == Path(path)

    def test_system_font_fallback(self):
        selector = FontSelector()
        path = "/usr/share/fonts/adobe-source-sans/SourceSansPro-Regular.otf"
        assert selector.select_the_best() == Path(path)

