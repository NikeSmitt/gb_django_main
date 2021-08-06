from django.db import models
from django.db.models import Sum

from geekshop import settings
from mainapp.models import Product


class BasketQuerySet(models.QuerySet):
    def delete(self):
        for object in self:
            object.product.quantity += object.quantity
            object.product.save()
            super(BasketQuerySet.__class__, self).delete()


class Basket(models.Model):
    objects = BasketQuerySet.as_manager()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='basket',
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(
        verbose_name='количество',
        default=0,
    )

    add_datetime = models.DateTimeField(
        verbose_name='время',
        auto_now_add=True,
    )

    is_deleted = models.BooleanField(
        default=False,
    )

    @property
    def total_price(self):
        return self.product.price * self.quantity

    @property
    def get_total_items(self):
        basket = Basket.objects.filter(user=self.user)
        return basket.aggregate(count=Sum('quantity'))['count']

    @property
    def get_total_sum(self):
        basket = Basket.objects.filter(user=self.user)
        return sum([b.total_price for b in basket])

    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()
