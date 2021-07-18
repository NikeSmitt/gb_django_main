from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from adminapp.forms import ProductCategoryCreateForm
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
class CategoryUpdateView(CategoryCreateView, UpdateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категория/редактировать'
        return context


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
