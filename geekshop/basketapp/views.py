from functools import reduce

from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from basketapp.get_basket import get_basket, get_total_items, get_total_sum

from basketapp.models import Basket
from mainapp.models import Product


def basket(request):

    context = {
        'basket': get_basket(request),
        'basket_items': get_total_items(request),
        'basket_total': get_total_sum(request),
    }
    return render(request, 'basketapp/basket.html', context)


def add_basket(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        current_basket = Basket.objects.filter(user=request.user, product=product).first()

        if not current_basket:
            current_basket = Basket(user=request.user, product=product)

        current_basket.quantity += 1
        current_basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_basket(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        current_basket = Basket.objects.filter(user=request.user, product=product).first()

        if current_basket.quantity == 1:
            current_basket.delete()
        else:
            current_basket.quantity -= 1
            current_basket.save()



    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
