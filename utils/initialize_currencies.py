from home.models import currency
import json

with open('utils/nomics_list.txt', 'r') as f:
    all_currencies = json.load(f)

i=0
for cur in all_currencies:
    print(i)
    i+=1
    Currency = currency(
        name = cur[0],
        symbol = cur[1],
        persian_name = cur[2].encode(),
        image_url= cur[3]
    )
    Currency.save()