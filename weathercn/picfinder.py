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

import regex
import io
import requests
from PIL import Image
import css_parser

class PicFinder(object):
    """获取css，提取背景

    天气图片是一张图片，通过background-postion来显示
    通过PIL剪切图片，来获取单个的天气图片

    :param str cssulr: css地址
    :param str imgurl: 图片地址
    :param regex.Regex reg: 匹配正则
    ```reg``` 匹配 {"d00".. "d10", "n00" .. "n10"}
              等天气style d开头为白天 n为夜晚
    :param int cropw: 图片宽度
    :param int croph: 图片高度
    :param dict mapping: 类别映射
    """

    def __init__(self):
        self.cssulr = "http://i.tq121.com.cn/c/weather2017/headStyle_1.css"
        self.imgurl = "https://i.tq121.com.cn/i/weather2017/weather_icon_d40l_b.png"
        self.reg = regex.compile(r"\.[nd]\d+$")
        self.cropw = 70
        self.croph = 77
        self.mapping = {}
        self.download()
        self.get_css()

    def download(self):
        """下载天气图片"""
        resp = requests.get(self.imgurl)
        picbin = io.BytesIO(resp.content)
        self.img = Image.open(picbin)

    def capture(self, kls, size=32):
        """根据类别剪切，默认大小为32x32, None时为默认大小"""
        box = self.mapping[kls]
        crop = self.img.crop(box)
        return crop.resize((size, size)) if size else crop

    def get_box(self, pos):
        """根据偏移量，获取PIL剪切矩阵"""
        width, height = pos.split()
        width = -int(width.replace("px", ""))
        height = -int(height.replace("px", ""))
        return (width, height, width + self.cropw, height + self.croph)

    def get_css(self):
        """获取css 并转换为mapping"""
        # 下载css
        sheet = css_parser.parseUrl(self.cssulr, validate=False, media=False)
        for rule in sheet.cssRules:
            if hasattr(rule, "selectorList"):
                for selector in rule.selectorList:
                    if self.reg.search(selector.selectorText):
                        sel = selector.selectorText.split('.')[1]
                        self.mapping[sel] = self.get_box(rule.style["background-position"])
