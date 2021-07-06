from django.shortcuts import render

from basketapp.models import Basket
from basketapp.get_basket import get_basket, get_total_items, get_total_sum


def index(request):
    items = []
    context = {
        'hot_items': items,
        'title': '$$$Geekshop$$$',
        'basket': get_basket(request),
        'basket_items': get_total_items(request),
        'basket_total': get_total_sum(request),

    }
    return render(request, 'index.html', context=context)


def contacts(request):
    context = {
        'title': 'Geekshop - Contacts',
        'basket': get_basket(request),
        'basket_items': get_total_items(request),
        'basket_total': get_total_sum(request),

    }
    return render(request, 'contacts.html', context=context)
