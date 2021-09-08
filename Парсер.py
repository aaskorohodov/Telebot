import requests, bs4

s = requests.get('https://www.ventusky.com/ru/yekaterinburg')
b = bs4.BeautifulSoup(s.text, "html.parser")
t = b.select(".temperature")
print(t)
w = t[0].getText().replace(" ", "")
print(w)

