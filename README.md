实时天气图片生成器
================================

### 介绍
根据中国天气网生成天气信息，抓取最近四天内的天气以及实时数据，
附带一些农历日历信息。

### 安装
* 从relase页面下载安装包

```
pip install weatherCN-0.1.0-py3-none-any.whl
```

### 使用
```
python -m weathercn <城市ID> <字体路径>
```
* 城市ID：如http://www.weather.com.cn/weather1d/101190401.shtml中的101190401
* 将会在用户文件夹下生成.cache/weatherCN目录
* weather.json为json文件
* weather.png为生成图片

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

### 效果预览
![Alt text](./screenshots/weather.png)
