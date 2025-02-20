"""We use this to get the text of the response to load for testing without hammering the API"""

import requests
from key import key

lat=52
lon=-4

url = f'http://api.openweathermap.org/data/3.0/onecall?lon={lon}&lat={lat}&exclude=minutely,alerts&appid={key}&units=metric'
res = requests.get(url)

print(res.text)
