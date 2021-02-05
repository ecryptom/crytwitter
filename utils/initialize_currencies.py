from home.models import currency, dollor
import json

with open('utils/new_nomics_list.txt', 'r') as f:
    all_currencies = json.load(f)

#save cryptocurrencies in database
i=0
for cur in all_currencies:
    print(i)
    i+=1
    Currency = currency(
        name = cur[0],
        symbol = cur[1],
        persian_name = cur[2],
        image_url= cur[3]
    )
    Currency.save()

#save dollor
d = dollor(rate=25700)
d.save()