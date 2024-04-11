from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    category_name = models.CharField(max_length=100, verbose_name='Наименование')
    category_description = models.CharField(verbose_name='Описание', **NULLABLE)

    def __str__(self):
        return f'{self.category_name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('category_name',)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    products_name = models.CharField(max_length=100, verbose_name='Наименование')
    products_description = models.TextField(verbose_name='Описание', **NULLABLE)
    image = models.ImageField(upload_to='products/', verbose_name='Изображение', **NULLABLE)
    price = models.IntegerField(verbose_name='Цена за покупку', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', **NULLABLE)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения', **NULLABLE)

    def __str__(self):
        return f'{self.category} {self.products_name}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('products_name',)
