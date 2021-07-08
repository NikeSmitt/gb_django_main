from django.shortcuts import render

from basketapp.get_basket import get_basket
from basketapp.models import Basket


def index(request):
    items = []

    context = {
        'hot_items': items,
        'title': '$$$Geekshop$$$',
        'basket': get_basket(request.user),
    }
    return render(request, 'index.html', context=context)


def contacts(request):
    basket = None
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    context = {
        'title': 'Geekshop - Contacts',
        'basket': get_basket(request.user),

    }
    return render(request, 'contacts.html', context=context)
