from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(
        verbose_name='имя',
        max_length=80,
        unique=True,
    )

    description = models.TextField(
        verbose_name='описание',
        blank=True
    )

    is_deleted = models.BooleanField(
        default=False,
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return f"{self.name} (id:{self.id})"


class Product(models.Model):
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE)

    name = models.CharField(
        verbose_name='наименование',
        max_length=80,
    )

    description = models.TextField(
        verbose_name='описание',
        blank=True,
    )

    image = models.ImageField(
        upload_to='products_images',
        blank=True
    )

    price = models.DecimalField(
        verbose_name='цена',
        max_digits=8,
        decimal_places=2,
        default=0
    )

    quantity = models.PositiveIntegerField(
        verbose_name='количество товара',
        default=0,
    )

    created = models.DateTimeField(
        auto_now_add=True
    )
    updated = models.DateTimeField(
        auto_now=True
    )

    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

    def __str__(self):
        return f'{self.name} ({self.category.name})'

    @staticmethod
    def get_items():
        return Product.objects.filter(is_deleted=False).order_by('category', 'name')
