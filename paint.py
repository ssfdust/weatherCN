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

from PIL import Image, ImageFont, ImageDraw

class Painter(object):
    """绘图模块

    根据WeatherParser获取到的信息绘制图片

    :param Image bg: 支持透明层的背景图片
    """

    def __init__(self, parser, picfinder):
        self.parser = parser
        self.picfinder = picfinder
        self.font = None
        self.bg = None
        self.img = None
        self.load()

    def load(self):
        """加载内容"""
        self.set_font()
        self.load_icons()
        self.bg = self.parser.bg.convert("RGBA")
        self.img = self.bg.copy()

    def set_font(self):
        """设置字体"""
        self.tifont = ImageFont.truetype("fonts/font.ttf", 60)
        self.font = ImageFont.truetype("fonts/font.ttf", 20)
        self.midfont = ImageFont.truetype("fonts/font.ttf", 30)
        self.lifont = ImageFont.truetype("fonts/font.ttf", 16)
        self.dayfont = ImageFont.truetype("fonts/font.ttf", 13)

    def paint(self):
        """画图"""
        # ================= hover =================
        hover = Image.new("RGBA", size=self.img.size)
        arc = ImageDraw.Draw(hover)
        arc.ellipse(((260, 75), (295, 110)), (177, 176, 79, int(255 * 0.6)))
        self.img = Image.alpha_composite(self.img, hover)
        # ================= header ================
        draw = ImageDraw.Draw(self.img)
        draw.text((268, 83),
                  self.parser.current["air_quality"],
                  font=self.lifont
                  )
        draw.text((30, 40), self.parser.current["temperature"],
                  font=self.tifont)
        draw.text((190, 65),
                  self.parser.current["cur_weather"],
                  font=self.midfont
                  )
        draw.text((230, 50),
                  "{}更新".format(self.parser.current["updateat"]),
                  font=self.lifont
                  )
        self.img.paste(
            self.picfinder.capture(
                self.parser.current["code"]
            ),
            (190, 40),
            mask=self.picfinder.capture(
                self.parser.current["code"]
            )
        )
        #  ============= body right ======================
        self.img.paste(
            self.picfinder.capture(
                self.parser.current["dcode"],
                None
            ),
            (160, 110),
            mask=self.picfinder.capture(
                self.parser.current["dcode"],
                None
            )
        )
        self.img.paste(
            self.picfinder.capture(
                self.parser.current["ncode"],
                48
            ),
            (240, 130),
            mask=self.picfinder.capture(
                self.parser.current["ncode"],
                48
            )
        )
        self.img.paste(self.up, (160, 190), mask=self.up)
        draw.text((178, 186),
                  self.parser.current["high"] + " ",
                  font=self.lifont
                  )
        self.img.paste(self.down, (230, 190), mask=self.down)
        draw.text((248, 186),
                  self.parser.current["low"] + " ",
                  font=self.lifont
                  )
        # ================ body left =================
        self.img.paste(self.wind, (35, 120), mask=self.wind)
        draw.text((60, 116),
                  "{} {}".format(self.parser.current["wind_direction"],
                                 self.parser.current["wind_level"]
                                 ),
                  font=self.lifont
                  )
        self.img.paste(self.water, (35, 145), mask=self.water)
        draw.text((60, 145),
                  "湿度 {}".format(self.parser.current["humidity"]),
                  font=self.lifont
                  )
        draw.text((60, 181),
                  self.parser.current["weather"],
                  font=self.lifont
                  )
        # ============ below ========================
        draw.line((35, 216, 290, 216), fill=(122, 109, 109, 250))
        draw.line((105, 216, 105, 366), fill=(122, 109, 109, 250))
        draw.line((200, 216, 200, 366), fill=(122, 109, 109, 250))
        draw.text((38, 226),
                  self.parser.forecast[0]["date"],
                  font=self.dayfont
                  )
        draw.text((42, 244),
                  self.parser.forecast[0]["weekday"],
                  font=self.dayfont
                  )
        self.img.paste(
            self.picfinder.capture(
                self.parser.forecast[0]['dcode']
            ),
            (42, 265),
            mask=self.picfinder.capture(
                self.parser.forecast[0]['dcode']
            )
        )
        draw.text((32, 300),
                  "{:^8}".format(self.parser.forecast[0]["weather"]),
                  font=self.dayfont
                  )
        draw.text((38, 320),
                  "{} ~ {}".format(self.parser.forecast[0]["high"],
                                   self.parser.forecast[0]["low"]),
                  font=self.dayfont
                  )

        draw.text((38 + 90, 226),
                  self.parser.forecast[1]["date"],
                  font=self.dayfont
                  )
        draw.text((42 + 90, 244),
                  self.parser.forecast[1]["weekday"],
                  font=self.dayfont
                  )
        self.img.paste(
            self.picfinder.capture(
                self.parser.forecast[1]['dcode']
            ),
            (42 + 90, 265),
            mask=self.picfinder.capture(
                self.parser.forecast[1]['dcode']
            )
        )
        draw.text((32 + 90, 300),
                  "{:^8s}".format(self.parser.forecast[1]["weather"]),
                  font=self.dayfont
                  )
        draw.text((38 + 90, 320),
                  "{} ~ {}".format(self.parser.forecast[1]["high"],
                                   self.parser.forecast[1]["low"]),
                  font=self.dayfont
                  )

        draw.text((38 + 180, 226),
                  self.parser.forecast[2]["date"],
                  font=self.dayfont
                  )
        draw.text((42 + 180, 244),
                  self.parser.forecast[2]["weekday"],
                  font=self.dayfont
                  )
        self.img.paste(
            self.picfinder.capture(
                self.parser.forecast[2]['dcode']
            ),
            (42 + 180, 265),
            mask=self.picfinder.capture(
                self.parser.forecast[2]['dcode']
            )
        )
        draw.text((32 + 180, 300),
                  "{:^8s}".format(self.parser.forecast[2]["weather"]),
                  font=self.dayfont
                  )
        draw.text((38 + 180, 320),
                  "{} ~ {}".format(self.parser.forecast[2]["high"],
                                   self.parser.forecast[2]["low"]),
                  font=self.dayfont
                  )

    def load_icons(self):
        """加载图标"""
        self.up = Image.open("icons/up.png").convert("RGBA")
        self.down = Image.open("icons/down.png").convert("RGBA")
        self.water = Image.open("icons/water.png").convert("RGBA")
        self.wind = Image.open("icons/wind.png").convert("RGBA")
        self.pm = Image.open("icons/pm.png").convert("RGBA")

    def crop(self):
        return self.img.crop((21, 28, 315, 358))
