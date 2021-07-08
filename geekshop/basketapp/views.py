from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from basketapp.get_basket import get_basket
from basketapp.models import Basket
from mainapp.models import Product
from django.contrib.auth.decorators import login_required


@login_required
def basket(request):
    context = {
        'basket': get_basket(request.user),
    }
    return render(request, 'basketapp/basket.html', context)


@login_required
def add_basket(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))

    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        current_basket = Basket.objects.filter(user=request.user, product=product).first()

        if not current_basket:
            current_basket = Basket(user=request.user, product=product)

        current_basket.quantity += 1
        current_basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove_basket(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        current_basket = Basket.objects.filter(user=request.user, product=product).first()
        current_basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def edit_basket(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        edit_basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            edit_basket_item.quantity = quantity
            edit_basket_item.save()
        else:
            edit_basket_item.delete()

        context = {
            'basket': Basket.objects.filter(user=request.user)
        }

        result = render_to_string('basketapp/includes/inc_basket_table.html', context)

        return JsonResponse({'result': result})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
