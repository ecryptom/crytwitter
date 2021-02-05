import requests
from bs4 import BeautifulSoup
from home.models import dollor


page = requests.get('https://eghtesadnews.com/markets/dollar')
soup = BeautifulSoup(page.content, 'html.parser')
dolor_rate = soup.find_all('table')[0].find_all('tr')[2].find_all('td')[1].text.replace(' تومان', '').replace(',', '')
dolor_rate = int(float(dolor_rate))

d = dollor.objects.get()
d.rate = dolor_rate
d.save()
