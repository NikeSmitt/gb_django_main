from django.shortcuts import render
from .models import ProductCategory
from .models import Product


def products(request):

    catalogs = ProductCategory.objects.all()
    items = Product.objects.all()

    context = {
        'title': 'Geekshop - Catalog',
        'catalog_items': items,
        'catalogs': catalogs
    }
    return render(request, 'mainapp/products.html', context=context)
# Create your views here.
