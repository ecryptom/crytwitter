import requests, json
from home.models import currency


all_currencies = currency.objects.all()

def update(currencies):
    global json, requests, currency
    symbols = [c.symbol for c in currencies]
    symbols = ','.join(symbols)
    response = requests.get(f'https://api.nomics.com/v1/currencies/ticker?key=e46fab48a3538b1ec642482aaa54fb68&ids={symbols}&interval=1d,7d')
    currencies_info = json.loads(response.content.decode().replace('\n', ''))
    for cur_info in currencies_info:
        try:
            cur = currency.objects.get(symbol=cur_info['id'])
            cur.price = cur_info['price']
            try:
                cur.market_cap = cur_info['market_cap']
            except:
                pass
            try:
                cur.daily_price_change_pct = float(cur_info['1d']['price_change_pct'])*100
            except:
                pass
            try:
                cur.weekly_price_change_pct = float(cur_info['7d']['price_change_pct'])*100
            except:
                pass
            try:
                cur.turnover = cur_info['1d']['volume']
            except:
                pass
            cur.save()
        except:
            pass


update(all_currencies[500:1000])
update(all_currencies[1000:1500])
update(all_currencies[1500:2000])
update(all_currencies[2000:2500])
update(all_currencies[2500:])
