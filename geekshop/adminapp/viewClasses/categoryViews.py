from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import F
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from adminapp.forms import ProductCategoryUpdateForm, ProductCategoryCreateForm
from adminapp.views import db_profile_by_type
from mainapp.models import ProductCategory


@method_decorator(login_required, name='dispatch')
class CategoriesView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/категории'
        return context


@method_decorator(login_required, name='dispatch')
class CategoryCreateView(CreateView):
    model = ProductCategory
    form_class = ProductCategoryCreateForm
    template_name = 'adminapp/category_create.html'
    success_url = reverse_lazy('admin_staff:categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категория/создать'
        return context


@method_decorator(login_required, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin_staff:categories')
    form_class = ProductCategoryUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категория/редактировать'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = ProductCategory
    success_url = reverse_lazy('admin_staff:categories')
    context_object_name = 'category_to_delete'
    template_name = 'adminapp/category_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категория/удаление'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)
