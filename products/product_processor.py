from .models import product

def get_products(request):
    products = product.objects.all()
    return {'products': products}