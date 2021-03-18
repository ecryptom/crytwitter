from home.models import statics

footer_text = statics.objects.get(name='footer_text').value
index_search_placeholder = statics.objects.get(name='index_search_placeholder').value
watchlist_header = statics.objects.get(name='watchlist_header').value
watchlist_search_placeholder = statics.objects.get(name='watchlist_search_placeholder').value

def global_variables(request):
    return {
        'footer_text': footer_text,
        'index_search_placeholder': index_search_placeholder,
        'watchlist_header': watchlist_header,
        'watchlist_search_placeholder': watchlist_search_placeholder,
        }