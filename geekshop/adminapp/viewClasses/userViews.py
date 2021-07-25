from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, UpdateView, ListView

from adminapp.forms import ShopUserAdminEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser


class UserCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_create.html'
    form_class = ShopUserRegisterForm
    success_url = reverse_lazy('admin_staff:users')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {
            'title': 'админка/пользователи'
        }
        context.update(kwargs)
        return super().get_context_data(**context)


class UserDeleteView(DeleteView):
    model = ShopUser
    success_url = reverse_lazy('admin_staff:users')
    template_name = 'adminapp/user_delete.html'
    context_object_name = 'user_to_delete'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {
            'title': 'пользователи/удалить'
        }
        context.update(kwargs)
        return super().get_context_data(**context)


class UserListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    context_object_name = 'objects'
    paginate_by = 3

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {
            'title': 'пользователи/создать'
        }
        context.update(kwargs)
        return super().get_context_data(**context)

    def get_queryset(self):
        return ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')


class UserUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    form_class = ShopUserAdminEditForm
    success_url = reverse_lazy('admin_staff:users')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {
            'title': 'админка/пользователи'
        }
        context.update(kwargs)
        return super().get_context_data(**context)
