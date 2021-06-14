# Copyright (c) 2019 RedLotus <ssfdust@gmail.com>
# Author: RedLotus <ssfdust@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .utils import centertxt


class Painter(object):
    """绘图模块

    根据WeatherParser获取到的信息绘制图片

    :param Image bg: 支持透明层的背景图片
    """

    def __init__(self, parser, picfinder, fontpath=""):
        self.parser = parser
        self.picfinder = picfinder
        self.fontpath = fontpath
        self.font = None
        self.bg = None
        self.img = None
        self.iconpath = Path(__file__).parent.joinpath("icons")
        self.load()

    def load(self):
        """加载内容"""
        self.set_font()
        self.load_icons()
        self.bg = self.parser.bg.convert("RGBA")
        self.img = self.bg.copy()

    def set_font(self):
        """设置字体"""
        self.tifont = ImageFont.truetype(self.fontpath, 60)
        self.font = ImageFont.truetype(self.fontpath, 20)
        self.midfont = ImageFont.truetype(self.fontpath, 30)
        self.lifont = ImageFont.truetype(self.fontpath, 16)
        self.dayfont = ImageFont.truetype(self.fontpath, 13)

    def paint(self):
        """画图"""
        # ================= hover =================
        hover = Image.new("RGBA", size=self.img.size)
        arc = ImageDraw.Draw(hover)
        arc.ellipse(
            ((260, 75), (295, 110)), (177, 176, 79, int(255 * 0.6))
        )
        self.img = Image.alpha_composite(self.img, hover)
        # ================= header ================
        draw = ImageDraw.Draw(self.img)
        draw.text(
            (268, 83), self.parser.current["air_quality"], font=self.lifont
        )
        draw.text(
            (30, 40), self.parser.current["temperature"], font=self.tifont
        )
        draw.text(
            (190, 65),
            self.parser.current["cur_weather"],
            font=self.midfont,
        )
        draw.text(
            (230, 50),
            "{}更新".format(self.parser.current["updateat"]),
            font=self.lifont,
        )
        self.img.paste(
            self.picfinder.capture(self.parser.current["code"]),
            (190, 40),
            mask=self.picfinder.capture(self.parser.current["code"]),
        )
        #  ============= body right ======================
        self.img.paste(
            self.picfinder.capture(self.parser.current["dcode"], None),
            (160, 110),
            mask=self.picfinder.capture(
                self.parser.current["dcode"], None
            ),
        )
        self.img.paste(
            self.picfinder.capture(self.parser.current["ncode"], 48),
            (240, 130),
            mask=self.picfinder.capture(self.parser.current["ncode"], 48),
        )
        self.img.paste(self.up, (160, 190), mask=self.up)
        draw.text(
            (178, 186), self.parser.current["high"] + " ", font=self.lifont
        )
        self.img.paste(self.down, (230, 190), mask=self.down)
        draw.text(
            (248, 186), self.parser.current["low"] + " ", font=self.lifont
        )
        # ================ body left =================
        self.img.paste(self.wind, (35, 120), mask=self.wind)
        draw.text(
            (60, 116),
            "{} {}".format(
                self.parser.current["wind_direction"],
                self.parser.current["wind_level"],
            ),
            font=self.lifont,
        )
        self.img.paste(self.water, (35, 145), mask=self.water)
        draw.text(
            (60, 145),
            "湿度 {}".format(self.parser.current["humidity"]),
            font=self.lifont,
        )
        draw.text(
            (60, 181), self.parser.current["weather"], font=self.lifont
        )
        # ============ below ========================
        draw.line((20, 216, 316, 216), fill=(122, 109, 109, 250))
        draw.line((118, 216, 118, 366), fill=(122, 109, 109, 250))
        draw.line((216, 216, 216, 366), fill=(122, 109, 109, 250))
        # ============ day one ======================
        draw.text(
            (33, 226),
            centertxt(self.parser.forecast[0]["date"]),
            font=self.dayfont,
        )
        draw.text(
            (33, 244),
            centertxt(self.parser.forecast[0]["weekday"]),
            font=self.dayfont,
        )
        self.img.paste(
            self.picfinder.capture(self.parser.forecast[0]["dcode"]),
            (50, 265),
            mask=self.picfinder.capture(self.parser.forecast[0]["dcode"]),
        )
        draw.text(
            (33, 300),
            centertxt(format(self.parser.forecast[0]["weather"])),
            font=self.dayfont,
        )
        draw.text(
            (33, 320),
            centertxt(
                "{} ~ {}".format(
                    self.parser.forecast[0]["high"],
                    self.parser.forecast[0]["low"],
                )
            ),
            font=self.dayfont,
        )

        # ================= day two ===================================
        draw.text(
            (33 + 100, 226),
            centertxt(self.parser.forecast[1]["date"]),
            font=self.dayfont,
        )
        draw.text(
            (33 + 100, 244),
            centertxt(self.parser.forecast[1]["weekday"]),
            font=self.dayfont,
        )
        self.img.paste(
            self.picfinder.capture(self.parser.forecast[1]["dcode"]),
            (50 + 100, 265),
            mask=self.picfinder.capture(self.parser.forecast[1]["dcode"]),
        )
        draw.text(
            (33 + 100, 300),
            centertxt(format(self.parser.forecast[1]["weather"])),
            font=self.dayfont,
        )
        draw.text(
            (33 + 100, 320),
            centertxt(
                "{} ~ {}".format(
                    self.parser.forecast[1]["high"],
                    self.parser.forecast[1]["low"],
                )
            ),
            font=self.dayfont,
        )

        # ================== day three ==========================
        draw.text(
            (33 + 200, 226),
            centertxt(self.parser.forecast[2]["date"]),
            font=self.dayfont,
        )
        draw.text(
            (33 + 200, 244),
            centertxt(self.parser.forecast[2]["weekday"]),
            font=self.dayfont,
        )
        self.img.paste(
            self.picfinder.capture(self.parser.forecast[2]["dcode"]),
            (50 + 200, 265),
            mask=self.picfinder.capture(self.parser.forecast[2]["dcode"]),
        )
        draw.text(
            (33 + 200, 300),
            centertxt(format(self.parser.forecast[2]["weather"])),
            font=self.dayfont,
        )
        draw.text(
            (33 + 200, 320),
            centertxt(
                "{} ~ {}".format(
                    self.parser.forecast[2]["high"],
                    self.parser.forecast[2]["low"],
                )
            ),
            font=self.dayfont,
        )

    def load_icons(self):
        """加载图标"""
        self.up = Image.open(self.iconpath.joinpath("up.png")).convert(
            "RGBA"
        )
        self.down = Image.open(self.iconpath.joinpath("down.png")).convert(
            "RGBA"
        )
        self.water = Image.open(
            self.iconpath.joinpath("water.png")
        ).convert("RGBA")
        self.wind = Image.open(self.iconpath.joinpath("wind.png")).convert(
            "RGBA"
        )
        self.pm = Image.open(self.iconpath.joinpath("pm.png")).convert(
            "RGBA"
        )

    def crop(self):
        return self.img.crop((21, 28, 315, 358))


def paint_icon(parser, picfinder, code=""):
    parser = parser
    picfinder = picfinder
    bg = Image.new("RGBA", size=(32, 32), color="#ffffff00")
    img = bg.copy()
    hover = Image.new("RGBA", size=img.size)
    img = Image.alpha_composite(img, hover)
    img.paste(
        picfinder.capture(parser.current["code"]),
        (0, 0),
        mask=picfinder.capture(parser.current["code"]),
    )
    return img
