from django.shortcuts import render, get_object_or_404

from basketapp.get_basket import get_basket
from .models import ProductCategory
from .models import Product
import random


def products(request, pk=None):
    catalogs = ProductCategory.objects.all()
    items = None
    title = None
    catalog_desc = None

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
        'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/products.html', context=context)


def product(request, pk):
    title = 'продукты'
    context = {
        'title': title,
        'catalogs': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/product.html', context=context)