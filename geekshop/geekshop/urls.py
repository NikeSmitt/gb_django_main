"""geekshop URL Configuration

The `urlpatterns` list routes URLs to viewClasses. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function viewClasses
    1. Add an import:  from my_app import viewClasses
    2. Add a URL to urlpatterns:  path('', viewClasses.home, name='home')
Class-based viewClasses
    1. Add an import:  from other_app.viewClasses import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import index, contacts
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_staff/', include('adminapp.urls', namespace='admin_staff')),
    path('', index, name='index'),
    path('contacts/', contacts, name='contacts'),
    path('products/', include('mainapp.urls', namespace='products')),
    path('basket/', include('basketapp.urls', namespace='basket')),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('orders/', include('ordersapp.urls', namespace='orders')),

    path('', include('social_django.urls', namespace='social')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
