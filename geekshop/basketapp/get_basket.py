from functools import reduce

from django.db.models import Sum, Count, Q

from basketapp.models import Basket


def get_basket(request):
    basket = None
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    return basket



def get_total_items(request):
    return get_basket(request).aggregate(count=Sum('quantity'))['count']


def get_total_sum(request):
    return reduce(lambda x, y: x + y, [b.total_price() for b in get_basket(request)])
