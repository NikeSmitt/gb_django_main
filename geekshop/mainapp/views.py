from django.shortcuts import render


def products(request):
    items = [
        {'name': 'Кросовки', 'price': 90, 'img': 'f-p-1.jpg'},
        {'name': 'Шнурки', 'price': 10, 'img': 'f-p-2.jpg'},
        {'name': 'Носки', 'price': 20, 'img': 'f-p-3.jpg'},
        {'name': 'Какая-то дичь', 'price': 14, 'img': 'f-p-4.jpg'},
        {'name': 'Красивая штука', 'price': 99, 'img': 'f-p-3.jpg'},
        {'name': 'Пустота', 'price': 290, 'img': 'f-p-4.jpg'},
        {'name': 'Опять', 'price': 990, 'img': 'f-p-2.jpg'},
    ]
    context = {
        'title': 'Geekshop - Catalog',
        'catalog_items': items,
    }
    return render(request, 'mainapp/products.html', context=context)
# Create your views here.
