import os.path
import json

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product

JSON_PATH = 'mainapp/json'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json')) as f:
        return json.load(f)


class Command(BaseCommand):
    def handle(self, *args, **options):

        categories = load_from_json('categories')

        ProductCategory.objects.all().delete()
        for category in categories:
            new_categoty = ProductCategory(**category)
            new_categoty.save()

        print(ProductCategory.objects.all())

        products = load_from_json('products')
        Product.objects.all().delete()

        for product in products:
            category_id = product['category']
            _category = ProductCategory.objects.get(id=category_id)
            product['category'] = _category
            new_product = Product(**product)
            new_product.save()

        user = ShopUser.objects.create_superuser('admin', 'admin@geekshop.local', '123', age='30')
