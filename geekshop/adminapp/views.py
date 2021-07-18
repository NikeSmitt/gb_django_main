from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test


from authapp.models import ShopUser
from mainapp.models import ProductCategory
from mainapp.models import Product

from authapp.forms import ShopUserRegisterForm
from adminapp.forms import ShopUserAdminEditForm, ProductCategoryCreateForm, ProductCreateForm


# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     title = 'админка/пользователи'
#
#     users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#
#     context = {
#         'title': title,
#         'objects': users_list
#     }
#
#     return render(request, 'adminapp/users.html', context)


# @user_passes_test(lambda u: u.is_superuser)
# def user_create(request):
#     title = 'пользователи/создать'
#
#     if request.method == 'POST':
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)
#
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:users'))
#     else:
#         user_form = ShopUserRegisterForm()
#
#     context = {
#         'title': title,
#         'user_form': user_form
#     }
#     return render(request, 'adminapp/user_create.html', context)


# @user_passes_test(lambda u: u.is_superuser)
# def user_update(request, pk):
#     title = 'пользователи/редактирование'
#
#     edit_user = get_object_or_404(ShopUser, pk=pk)
#
#     if request.method == 'POST':
#         edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
#         if edit_form.is_valid():
#             edit_form.save()
#
#             return HttpResponseRedirect(reverse('admin_staff:users'))
#     else:
#         edit_form = ShopUserAdminEditForm(instance=edit_user)
#
#     context = {
#         'title': title,
#         'user_form': edit_form,
#     }
#     return render(request, 'adminapp/user_update.html', context)


# @user_passes_test(lambda u: u.is_superuser)
# def user_delete(request, pk):
#     title = 'пользователи/удаление'
#
#     user = get_object_or_404(ShopUser, pk=pk)
#
#     if request.method == 'POST':
#         user.is_deleted = True
#         user.is_active = False
#         user.save()
#         return HttpResponseRedirect(reverse('admin_staff:users'))
#
#     context = {'title': title, 'user_to_delete': user}
#
#     return render(request, 'adminapp/user_delete.html', context)


# @user_passes_test(lambda u: u.is_superuser)
# def categories(request):
#     title = 'админка/категории'
#
#     categories_list = ProductCategory.objects.all()
#
#     context = {
#         'title': title,
#         'objects': categories_list
#     }
#
#     return render(request, 'adminapp/categories.html', context)


# @user_passes_test(lambda u: u.is_superuser)
# def category_create(request):
#     title = 'категория/создать'
#
#     if request.method == 'POST':
#         category_form = ProductCategoryCreateForm(request.POST, request.FILES)
#
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:categories'))
#     else:
#         category_form = ProductCategoryCreateForm()
#
#     context = {
#         'title': title,
#         'category_form': category_form
#     }
#     return render(request, 'adminapp/category_create.html', context)


# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):
#     title = 'категория/редактировать'
#
#     category_to_edit = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         category_form = ProductCategoryCreateForm(request.POST, request.FILES, instance=category_to_edit)
#
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:categories'))
#     else:
#         category_form = ProductCategoryCreateForm(instance=category_to_edit)
#
#     context = {
#         'title': title,
#         'category_form': category_form
#     }
#     return render(request, 'adminapp/category_create.html', context)


# @user_passes_test(lambda u: u.is_superuser)
# def category_delete(request, pk):
#     title = 'категории/удаление'
#
#     category_to_delete = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         category_to_delete.is_deleted = True
#         category_to_delete.is_active = False
#         category_to_delete.save()
#         return HttpResponseRedirect(reverse('admin_staff:categories'))
#
#     context = {'title': title, 'category_to_delete': category_to_delete}
#
#     return render(request, 'adminapp/category_delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    title = 'админка/продукт'

    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    context = {
        'title': title,
        'category': category,
        'objects': products_list,
    }

    return render(request, 'adminapp/products.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    title = 'продукты/создание'

    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        product_form = ProductCreateForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()

            return HttpResponseRedirect(reverse('admin_staff:products', args=[pk]))
    else:
        product_form = ProductCreateForm(initial={'category': category})

    context = {
        'title': title,
        'update_form': product_form,
        'category': category,
        'is_update': False,
    }
    return render(request, 'adminapp/product_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_read(request, pk):
    title = 'продукты/подробнее'

    product = get_object_or_404(Product, pk=pk)

    context = {
        'title': title,
        'product': product,
    }

    return render(request, 'adminapp/product_read.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = 'продукты/редактирование'

    edit_product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        edit_form = ProductCreateForm(request.POST, request.FILES, instance=edit_product)
        if edit_form.is_valid():
            edit_form.save()

            return HttpResponseRedirect(reverse('admin_staff:products', args=[edit_product.category.id]))
    else:
        edit_form = ProductCreateForm(instance=edit_product)

    context = {
        'title': title,
        'update_form': edit_form,
        'is_update': True,
        'category': edit_product.category,
    }
    return render(request, 'adminapp/product_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    title = 'продукт/удаление'

    product_to_delete = get_object_or_404(Product, pk=pk)
    category_id = product_to_delete.category_id
    products_list = Product.objects.filter(category__pk=category_id)

    context = {
        'title': title,
        'category_id': category_id,
        'objects': products_list,
        'product_to_delete': product_to_delete,
    }

    if request.method == 'POST':
        product_to_delete.is_deleted = True
        product_to_delete.is_active = False
        product_to_delete.save()
        return HttpResponseRedirect(reverse('admin_staff:products', kwargs={'pk': category_id}))

    return render(request, 'adminapp/product_delete.html', context)
