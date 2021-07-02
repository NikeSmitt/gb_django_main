from django.urls import path
from .views import login
from .views import logout
from .views import edit
from .views import register

app_name = 'authapp'

urlpatterns = [

    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('edit/', edit, name='edit'),

]
