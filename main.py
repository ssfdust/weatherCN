import css_parser
import io
import regex
import requests
import arrow
from PIL import Image
import json

class WeatherRepoter(object):
    def __init__(self, year, month, location):
        self.url = self.urlmaker(year, month, location)
        self.cur_url = self.cururlmaker(location)
        self.headers = self.header_maker(location)
        self.calendar = None
        self.current = None
        self.forecast = None
        self.get_data()
        self.filter_calendar()

    def get_data(self):
        params = {'_': arrow.get().timestamp * 1000}
        resp = requests.get(self.url, headers=self.headers, params=params)
        self.calendar = self.parse(resp.content)
        resp = requests.get(self.cur_url, headers=self.headers, params=params)
        self.current = self.parse(resp.content)

    def cururlmaker(self, location):
        return f"http://d1.weather.com.cn/sk_2d/{location}.html?_=1557934146877"

    def filter_calendar(self):
        self.forecast = list(filter(lambda x: True if x['date'] in self.datelst else False, self.calendar))

    @property
    def datelst(self):
        now = arrow.now()
        return [now.shift(days=i).format('YYYYMMDD') for i in range(1, 4)]

    def parse(self, data):
        data = data.decode('utf-8')
        jsonstr = regex.search(r"[\s=]([{\[].*?[}\]])$", data).group(1)
        return json.loads(jsonstr, encoding='utf-8')

    def header_maker(self, location):
        return {"Referer": f"http://www.weather.com.cn/weather40dn/{location}.shtml",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0"}

    def urlmaker(self, year, month, location):
        return f"http://d1.weather.com.cn/calendarFromMon/{year}/{location}_{year}{month:02}.html"

class PicFinder(object):
    def __init__(self):
        self.cssulr = "http://i.tq121.com.cn/c/weather2017/headStyle_1.css"
        self.imgurl = "https://i.tq121.com.cn/i/weather2017/weather_icon_d40l_b.png"
        self.reg = regex.compile(r"\.d\d+$")
        self.cropw = 70
        self.croph = 77
        self.mapping = {}
        self.download()
        self.get_css()

    def download(self):
        resp = requests.get(self.imgurl)
        picbin = io.BytesIO(resp.content)
        self.img = Image.open(picbin)

    def capture(self, kls):
        box = self.mapping[kls]
        crop = self.img.crop(box)
        return crop.resize((32, 32))

    def get_box(self, pos):
        width, height = pos.split()
        width = -int(width.replace("px", ""))
        height = -int(height.replace("px", ""))
        return (width, height, width + self.cropw, height + self.croph)

    def get_css(self):
        sheet = css_parser.parseUrl(self.cssulr)
        for rule in sheet.cssRules:
            if hasattr(rule, "selectorList"):
                for selector in rule.selectorList:
                    if self.reg.search(selector.selectorText):
                        sel = selector.selectorText.split('.')[1]
                        self.mapping[sel] = self.get_box(rule.style["background-position"])


p = PicFinder()
pic = p.capture('d00')
wr = WeatherRepoter(2019, 5, 101190401)
from pprint import pprint  # noqa
pprint(wr.current)
