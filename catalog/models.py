from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Наименование категории",
        help_text="Введите название категории",
    )
    description = models.TextField(
        verbose_name="Описание категории",
        help_text="Введите описание категории",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Наименование продукта",
        help_text="Введите название продукта",
    )
    description = models.TextField(
        verbose_name="Описание продукта", help_text="Введите описание продукта"
    )
    image = models.ImageField(
        upload_to="products/photo",
        blank=True,
        null=True,
        verbose_name="Изображение продукта",
        help_text="Загрузите изображение продукта",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория продукта",
        help_text="Введите название категории продукта",
        blank=True,
        null=True,
        related_name="products",
    )
    price = models.PositiveIntegerField(
        verbose_name="Цена за покупку", help_text="Введите цену за покупку"
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
        help_text="Укажите дату создания",
    )
    updated_at = models.DateTimeField(
        verbose_name="Дата последнего изменения",
        auto_now=True,
        help_text="Укажите дату последнего изменения",
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              verbose_name='Автор', blank=True, null=True,
                              related_name='products')
    is_published = models.BooleanField(default=False,
                                       verbose_name='Доступно публике')

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["category", "name"]
        permissions = [
            ('product_set_published_status', 'Публиковать товар'),
            ('product_change_description', 'Изменять описание товара'),
            ('product_change_category', 'Изменять категорию товара'),
        ]

    def __str__(self):
        return self.name


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='versions', verbose_name='продукт')
    version_number = models.CharField(max_length=100,
                                      verbose_name='номер версии')
    version_name = models.CharField(max_length=100,
                                    verbose_name='название версии')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.version_name} - {self.version_number}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
