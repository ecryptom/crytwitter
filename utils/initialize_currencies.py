from home.models import currency, dollor, statics
from accounts.models import user
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

#save arztwitter user
if not user.objects.filter(username="arztwitter"):
    User = user(
        username='arztwitter',
        name='کاربر ارزتوییتر',
        password='arz0990twiitterk@34f!3344',
        phone='09909799875',
        verified_phone=True
    )
    User.save()

#initialze static texts in db
statics(name='footer_text', descreption="متن فوتر").save()
statics(name='index_search_placeholder', descreption="متن باکس جست و جوی صفحه اصلی").save()
statics(name='watchlist_header', descreption="متن صفحه دیده بان").save()
statics(name='watchlist_search_placeholder', descreption="متن باکس جست و جوی صفحه دیده بان").save()
statics(name='views_count', descreption="تعداد کل بازدید سایت", value=100).save()