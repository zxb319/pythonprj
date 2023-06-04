import json
import re

import requests

url = 'http://weathernew.pae.baidu.com/weathernew/pc?query=%E4%B8%8A%E6%B5%B7%E5%A4%A9%E6%B0%94&srcid=4982'

resp = requests.get(url)

res = re.search(r'data\["weather15DayData"\]=(\[[^\[\]]+\])', resp.text).group(1)
weathers = json.loads(res)

res = re.search(r'data\["temperatureDayList"\]=(\[[^\[\]]+\])', resp.text).group(1)
max_temperatures = json.loads(res)

res = re.search(r'data\["temperatureNightList"\]=(\[[^\[\]]+\])', resp.text).group(1)
min_temperatures = json.loads(res)

print(*[{'日期': w['date'], '天气': w['weatherText'], '气温': f'{minw["temperature"]}-{maxw["temperature"]}'} for w, minw, maxw in zip(weathers, min_temperatures, max_temperatures)],
      sep='\n')
