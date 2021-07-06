from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from .models import ProductCategory
from .models import Product
from basketapp.get_basket import get_basket, get_total_items, get_total_sum
import random


def products(request, pk=None):
    catalogs = ProductCategory.objects.all()
    items = None
    title = None
    catalog_desc = None
    basket = get_basket(request)

    if pk is not None:
        if pk == 0:
            items = Product.objects.all()
            title = 'Все'
            catalog_desc = 'Все, что у нас есть'
        else:
            items = Product.objects.filter(category__pk=pk)
            selected_category = get_object_or_404(ProductCategory, pk=pk)
            print(selected_category)
            title = selected_category.name
            catalog_desc = selected_category.description

    else:
        title = 'our best sellers'
        catalog_desc = 'Being something that everyone does literally every day'
        items = random.sample(list(Product.objects.all()), 2)

    context = {
        'title': title,
        'catalog_items': items,
        'catalogs': catalogs,
        'catalog_desc': catalog_desc,
        'basket': get_basket(request),
        'basket_items': get_total_items(request),
        'basket_total': get_total_sum(request),
    }
    return render(request, 'mainapp/products.html', context=context)
# Create your views here.
