实时天气图片生成器
================================

### 介绍
根据中国天气网生成天气信息，抓取最近四天内的天气以及实时数据，
附带一些农历日历信息。

### 效果预览
![Alt text](https://github.com/ssfdust/weatherCN/raw/master/screenshots/weather.png)

### 安装

```
pip install py-weathercn --user
```

### 使用
```
weathercn -f <自定义字体> <城市ID或城市名>
```
* 城市ID：如http://www.weather.com.cn/weather1d/101190401.shtml 中的101190401
* 将会在用户文件夹下生成.cache/weatherCN目录，为缓存weather.json, weather.png, icon.png文件
* weather.json为json文件
* weather.png为生成图片
* icon.png为当前天气的icon图标（例如用于waybar等）
* 自定义字体支持路径，fontconfig

### json展示
```json
{
    "current": {
        "humidity": "79%",
        "wind_direction": "东南风 ",
        "wind_level": "3级",
        "air_quality": "29",
        "air_pressure": "1004",
        "updateat": "09:55",
        "cur_weather": "阴",
        "temperature": "23 ℃",
        "weather": "小雨转阴",
        "dcode": "d07",
        "ncode": "d02",
        "high": "25 ℃",
        "low": "21 ℃",
        "code": "d02",
        "unsuited": "修坟-安葬-入宅-安门-安床",
        "suited": "嫁娶-移徙-赴任-除服-纳采",
        "lunar": "四月十三",
        "shizhai": ""
    },
    "forcast": [
        {
            "date": "五月18日",
            "weekday": "星期六",
            "high": "25",
            "low": "18",
            "dcode": "d01",
            "ncode": "n01",
            "weather": "多云"
        },
        {
            "date": "五月19日",
            "weekday": "星期日",
            "high": "27",
            "low": "20",
            "dcode": "d02",
            "ncode": "n01",
            "weather": "阴转多云"
        },
        {
            "date": "五月20日",
            "weekday": "星期一",
            "high": "23",
            "low": "16",
            "dcode": "d01",
            "ncode": "n00",
            "weather": "多云转晴"
        }
    ]
}
```

### json释义
1. humidity: 湿度
2. wind_level: 风级
3. wind_direction: 风向
4. air_quality: 空气质量
5. air_pressure: 气压
6. updateat: 更新时间
7. cur_weather: 当前天气
8. temperature: 当前气温
9. weather: 小雨转阴,
10. dcode: 白天天气图标
11. ncode: 夜间天气图标
12. high: 最高温度
13. low: 最低温度
14. code: 当前天气图标
15. unsuited: 不宜
16. suited: 宜
17. lunar: 农历
18. shizhai: 是否是地藏十斋日
19. date: 日期

