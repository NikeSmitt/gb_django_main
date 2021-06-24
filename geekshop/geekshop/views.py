from django.shortcuts import render


def index(request):
    items = [
        {'name': 'Кросовки', 'price': 90, 'img': 'f-p-1.jpg'},
        {'name': 'Штаны', 'price': 10, 'img': 'f-p-2.jpg'},
        {'name': 'Носки', 'price': 20, 'img': 'f-p-2.jpg'},
        {'name': 'Что-то', 'price': 14, 'img': 'f-p-1.jpg'},
    ]
    context = {
        'hot_items': items,
        'title': '$$$Geekshop$$$',
    }
    return render(request, 'index.html', context=context)


def contacts(request):
    context = {
        'title': 'Geekshop - Contacts'
    }
    return render(request, 'contacts.html', context=context)
