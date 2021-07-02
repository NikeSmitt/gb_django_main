from django.shortcuts import render


def index(request):
    items = [

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
