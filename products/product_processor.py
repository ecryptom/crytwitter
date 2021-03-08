from .models import product_group

def get_product_groups(request):
    groups = product_group.objects.all()
    return {'product_groups': groups}