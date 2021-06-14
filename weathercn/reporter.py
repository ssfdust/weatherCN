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
"""获取天气预报

"""

import arrow
import requests
import json
import regex

class WeatherRepoter(object):
    """
    获取天气预报

    :param int year: 年份
    :param int month: 月份
    :param str location: 地区

    ```location``` 地区参数可以为整形也可以为字符串
    """

    def __init__(self, year, month, location):
        self.url = self.urlmaker(year, month, location)
        self.cur_url = self.cururlmaker(location)
        self.headers = self.header_maker(location)
        self.calendar = None  # 日历字典
        self.current = None  # 当前天气字典
        self.forecast = None  # 自今日起后4日日历字典
        self.get_data()
        self.filter_calendar()

    def get_data(self):
        """
        获取日历数据以及实时数据

        访问地址时，需要带上时间参数以及Referer的headers
        """
        # 生成时间参数
        params = {'_': arrow.get().timestamp * 1000}
        # 获取日历数据
        resp = requests.get(self.url, headers=self.headers, params=params)
        self.calendar = self.parse(resp.content)
        # 获取实时数据
        resp = requests.get(self.cur_url, headers=self.headers, params=params)
        self.current = self.parse(resp.content)

    def cururlmaker(self, location):
        """当前天气URL"""
        return f"http://d1.weather.com.cn/sk_2d/{location}.html"

    def filter_calendar(self):
        """过滤最近四天的数据"""
        forecast = list(filter(lambda x: True if x["date"] in self.datelst else False, self.calendar))
        # 重新排序
        forecast.sort(key=lambda x: x["date"])
        self.forecast = forecast

    @property
    def datelst(self):
        """最近四天日期"""
        now = arrow.now()
        return [now.shift(days=i).format("YYYYMMDD") for i in range(0, 4)]

    def parse(self, data):
        """提取json字符串，并转为dict"""
        data = data.decode("utf-8")
        jsonstr = regex.search(r"[\s=]([{\[].*?[}\]])$", data).group(1)
        return json.loads(jsonstr)

    def header_maker(self, location):
        """生成合法headers"""
        return {"Referer": f"http://www.weather.com.cn/weather40dn/{location}.shtml",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0"}

    def urlmaker(self, year, month, location):
        """日历天气URL"""
        return f"http://d1.weather.com.cn/calendarFromMon/{year}/{location}_{year}{month:02}.html"
