#!/bin/env python3
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

from argparse import ArgumentParser
from datetime import datetime

from .paint import Painter, paint_icon
from .parser import WeatherParser
from .picfinder import PicFinder
from .reporter import WeatherRepoter
from .utils import cache_path


def main():
    parser = ArgumentParser()
    parser.add_argument("location", help="地址")
    parser.add_argument("fontpath", help="字体路径")
    parser.add_argument("-i", "--icon", action="store_true", default=False)
    args = parser.parse_args()

    p = PicFinder()
    time = datetime.now()
    wr = WeatherRepoter(time.year, time.month, args.location)
    par = WeatherParser(wr.current, wr.forecast)
    par.parse()
    par.to_json(cache_path("weather.json"))
    if args.location and args.fontpath:
        pa = Painter(par, p, args.fontpath)
        pa.load()
        pa.paint()
        bg = pa.crop()
        bg.save(cache_path("weather.png"))
    if args.icon:
        icon = paint_icon(par, p)
        icon.save(cache_path("icon.png"))
