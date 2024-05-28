from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    category_name = models.CharField(max_length=100, verbose_name='наименование')
    category_description = models.CharField(verbose_name='описание', **NULLABLE)

    def __str__(self):
        return f'{self.category_name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('pk',)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='категория')
    products_name = models.CharField(max_length=100, verbose_name='наименование')
    products_description = models.TextField(verbose_name='описание', **NULLABLE)
    image = models.ImageField(upload_to='products/', verbose_name='изображение', **NULLABLE)
    price = models.IntegerField(verbose_name='цена за покупку', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания', **NULLABLE)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='дата последнего изменения', **NULLABLE)

    def __str__(self):
        return f'{self.products_name}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('pk',)


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='продукт')
    version_number = models.IntegerField(verbose_name='номер версии', **NULLABLE)
    version_name = models.CharField(max_length=100, verbose_name='название версии', **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name='признак текущей версии', **NULLABLE)

    def __str__(self):
        return f'{self.version_name}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
        ordering = ('pk',)
