from django.urls import path
from basketapp.views import basket, add_basket, remove_basket, edit_basket


app_name = 'basketapp'

urlpatterns = [

    path('', basket, name='index'),
    path('add/<int:pk>', add_basket, name='add'),
    path('remove/<int:pk>', remove_basket, name='remove'),
    path('edit/<int:pk>/<int:quantity>', edit_basket, name='edit'),

]
