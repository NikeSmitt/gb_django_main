from django.shortcuts import render, get_object_or_404

from basketapp.get_basket import get_basket
from .models import ProductCategory
from .models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random


def products(request, pk=None, page=1):
    catalogs = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            _products = Product.objects.filter(is_deleted=False)
            title = 'Все'
            catalog_desc = 'Все, что у нас есть'
        else:
            _products = Product.objects.filter(is_deleted=False, category__pk=pk)
            selected_category = get_object_or_404(ProductCategory, pk=pk)
            title = selected_category.name
            catalog_desc = selected_category.description

    else:
        title = 'our best sellers'
        catalog_desc = 'Being something that everyone does literally every day'
        _products = list(Product.objects.filter(is_deleted=False))
        if len(_products):
            _products = random.sample(_products, min(len(_products), 2))

    paginator = Paginator(_products, 3)
    try:
        products_paginator = paginator.page(page)

    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)


    context = {
        'title': title,
        'products': products_paginator,
        'catalogs': catalogs,
        'catalog_desc': catalog_desc,
        'basket': get_basket(request.user),
        'category': pk,
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
