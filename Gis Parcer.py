import requests, bs4

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}
s = requests.get('https://www.gismeteo.ru/weather-yekaterinburg-4517/month/', headers=headers)
b = bs4.BeautifulSoup(s.text, "html.parser")
t = b.select(".value unit unit_temperature_c")
#w = t[0].getText().replace(" ", "")
print(t)


