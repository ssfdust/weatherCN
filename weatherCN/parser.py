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

import io

import arrow
import json
import requests
from PIL import Image

class WeatherParser(object):

    def __init__(self, current, forecast):
        self._current = current
        self.current = None
        self._forecast = forecast
        self.forecast = None
        self.sz = ["初一", "初八", "十四",
                   "十五", "十八", "廿三",
                   "廿四", "廿八", "廿九", "三十"]
        self.bg = None

    def parse(self):
        """进行处理"""
        self.parse_current()
        self.get_background()
        self.parse_forecast()

    def to_json(self, fpath=None):
        data = {
            "current": self.current,
            "forcast": self.forecast
        }
        if fpath:
            with open(fpath, 'w') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        else:
            return json.dumps(data, indent=4, ensure_ascii=False)

    def to_cnday(self, date):
        """转换日期为星期"""
        return arrow.get(date, "YYYYMMDD").format("dddd", "zh_CN")

    def to_cndate(self, date):
        """转换为月日"""
        return arrow.get(date, "YYYYMMDD").format("MMMMD日", "zh_CN")

    def parse_forecast(self):
        """处理未来三天天气预报内容"""
        self.forecast = [
            {
                "date": self.to_cndate(item["date"]),
                "weekday": self.to_cnday(item["date"]),
                "high": item["max"],
                "low": item["min"],
                "dcode": "d{}".format(item["c1"]),
                "ncode": "n{}".format(item["c2"]),
                "weather": item["w1"]
            } for item in self._forecast[1:]
        ]

    def parse_current(self):
        """处理当前天气内容"""
        self.current = {
            "humidity": self._current["SD"],
            "wind_direction": self._current["WD"],
            "wind_level": self._current["WS"],
            "air_quality": self._current["aqi_pm25"],
            "air_pressure": self._current["qy"],
            "updateat": self._current["time"],
            "cur_weather": self._current['weather'],
            "temperature": "%s ℃" % self._current["temp"],
            "weather": self._forecast[0]["w1"],
            "dcode": "d{}".format(self._forecast[0]["c1"]),
            "ncode": "d{}".format(self._forecast[0]["c2"]),
            "high": "%s ℃" % self._forecast[0]["max"],
            "low": "%s ℃" % self._forecast[0]["min"],
            "code": self._current["weathercode"],
            "unsuited": self._forecast[0]["alins"],
            "suited": self._forecast[0]["als"],
            "lunar": "{}{}".format(self._forecast[0]["nlyf"],
                                   self._forecast[0]["nl"]),
            "shizhai": "十斋日" if self._forecast[0]["nl"] in self.sz else ""
        }

    def get_background(self):
        """获取背景"""
        code = self.current["code"][1:]
        bg = "weatherBg01" if code not in self.mapping else self.mapping[code]

        url = "https://i.tq121.com.cn/i/weather2017/{}.jpg".format(bg)
        resp = requests.get(url)
        self.bg = Image.open(io.BytesIO(resp.content))

    @property
    def mapping(self):
        """编码背景映射"""
        return {
            "01": "weatherBg02",
            "02": "weatherBg03",
            "03": "weatherBg04",
            "06": "weatherBg04",
            "07": "weatherBg04",
            "08": "weatherBg04",
            "09": "weatherBg04",
            "10": "weatherBg04",
            "11": "weatherBg04",
            "12": "weatherBg04",
            "19": "weatherBg04",
            "21": "weatherBg04",
            "22": "weatherBg04",
            "23": "weatherBg04",
            "24": "weatherBg04",
            "25": "weatherBg04",
            "301": "weatherBg04",
            "97": "weatherBg04",
            "04": "weatherBg05",
            "05": "weatherBg05",
            "13": "weatherBg06",
            "14": "weatherBg06",
            "15": "weatherBg06",
            "16": "weatherBg06",
            "17": "weatherBg06",
            "26": "weatherBg06",
            "27": "weatherBg06",
            "28": "weatherBg06",
            "302": "weatherBg06",
            "98": "weatherBg06",
            "18": "weatherBg07",
            "32": "weatherBg07",
            "49": "weatherBg07",
            "57": "weatherBg07",
            "58": "weatherBg07",
            "20": "weatherBg08",
            "31": "weatherBg08",
            "29": "weatherBg09",
            "30": "weatherBg09",
            "53": "weatherBg10",
            "54": "weatherBg10",
            "55": "weatherBg10",
            "56": "weatherBg10"
        }
