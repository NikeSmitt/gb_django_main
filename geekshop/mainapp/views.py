from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404

from basketapp.get_basket import get_basket
from .models import ProductCategory
from .models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_deleted=False)
            cache.set(key, links_menu)
            return links_menu
    else:
        return ProductCategory.objects.filter(is_deleted=False)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
            return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_deleted=False, category__is_deleted=False).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_deleted=False, category__is_deleted=False).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = 'products_orederd_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_deleted=False, category__is_deleted=False).order_by('price')
            cache.set(key, products)
            return products
    else:
        return Product.objects.filter(is_deleted=False, category__is_deleted=False).order_by('price')


def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_deleted=False, category__is_deleted=False).order_by(
                'price')
            cache.set(key, products)
            return products
    else:
        return Product.objects.filter(category__pk=pk, is_deleted=False, category__is_deleted=False).order_by('price')


def products(request, pk=None, page=1):
    catalogs = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            _products = get_products_in_category_ordered_by_price()
            title = 'Все'
            catalog_desc = 'Все, что у нас есть'
        else:
            _products = get_products_in_category_ordered_by_price(pk)
            selected_category = get_category(pk)
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
        'category': pk,
    }
    return render(request, 'mainapp/products.html', context=context)


def product(request, pk):
    title = 'продукты'
    context = {
        'title': title,
        'catalogs': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
    }
    return render(request, 'mainapp/product.html', context=context)
