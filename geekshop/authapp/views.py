from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from django.urls import reverse
from django.core.mail import send_mail

from geekshop import settings
from .forms import ShopUserLoginForm, ShopUserProfileEditForm
from .forms import ShopUserRegisterForm

from .forms import ShopUserEditForm
from .models import ShopUser


def send_verify_email(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
    title = f'Активация на сайте пользователя - {user.username}'
    message = f'Для активанции вашей учетной записи {user.username} на портале {settings.DOMAIN_NAME}' \
              f'перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'
    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def login(request):
    title = 'вход'

    _next = request.GET['next'] if 'next' in request.GET.keys() else ''

    login_form = ShopUserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(
            username=username,
            password=password
        )

        if user and user.is_active:
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            return HttpResponseRedirect(reverse('index'))

    context = {
        'title': title,
        'login_form': login_form,
        'next': _next,
    }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            if send_verify_email(user):
                print('Message sent')
            else:
                print('Message sent ERROR!')
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()

    context = {
        'title': title,
        'register_form': register_form
    }

    return render(request, 'authapp/register.html', context)


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user)
            return render(request, 'authapp/verification.html')
        else:
            print(f'error activation user {user.username}')
            return render(request, 'authapp/verification.html')
    except Exception as err:
        print(f'error activation user: {err.args}')
        return HttpResponseRedirect(reverse('index'))


@transaction.atomic
def edit(request):
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = ShopUserProfileEditForm(request.POST, request.FILES, instance=request.user.shopuserprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)

    context = {
        'title': title,
        'edit_form': edit_form,
        'profile_form': profile_form,
    }

    return render(request, 'authapp/edit.html', context)
