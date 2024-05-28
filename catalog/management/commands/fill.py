import json
import pathlib

from django.core.management import BaseCommand
from django.db import connection

from blog.models import Blog
from catalog.models import Category, Product, Version

ROOT = pathlib.Path(__file__).parent.parent.parent.parent
DATA_CATEGORY = pathlib.Path(ROOT, 'data', 'category.json')
DATA_PRODUCT = pathlib.Path(ROOT, 'data', 'product.json')
DATA_BLOG = pathlib.Path(ROOT, 'data', 'blog.json')
DATA_VERSION = pathlib.Path(ROOT, 'data', 'version.json')


class Command(BaseCommand):

    @staticmethod
    def json_read(path) -> list:
        # Здесь мы получаем данные из фикстур с категориями
        with open(path, encoding="utf-8") as file:
            file_info = json.load(file)
        return [info for info in file_info]

    def handle(self, *args, **options):
        # Очистка базы данных перед заполнением
        Category.objects.all().delete()
        Product.objects.all().delete()
        Blog.objects.all().delete()
        Version.objects.all().delete()

        category_for_create = []
        product_for_create = []
        blog_for_create = []
        version_for_create = []

        with connection.cursor() as cursor:
            cursor.execute(
                "TRUNCATE TABLE catalog_category, catalog_product, blog_blog, catalog_version RESTART IDENTITY "
                "CASCADE;")

        # Заполнение категорий
        for category in Command.json_read(DATA_CATEGORY):
            category_fields = category.get('fields')
            category_for_create.append(
                Category(category_name=category_fields.get('category_name'),
                         category_description=category_fields.get('category_description'))
            )
        Category.objects.bulk_create(category_for_create)

        # Заполнение продуктов
        for product in Command.json_read(DATA_PRODUCT):
            product_fields = product.get('fields')
            product_for_create.append(
                Product(category=Category.objects.get(pk=product_fields.get('category')),
                        products_name=product_fields.get('products_name'),
                        products_description=product_fields.get('products_description'),
                        image=product_fields.get('image'),
                        price=product_fields.get('price'))
            )
        Product.objects.bulk_create(product_for_create)

        # Заполнение блога
        for blog in Command.json_read(DATA_BLOG):
            blog_fields = blog.get('fields')
            blog_for_create.append(
                Blog(title=blog_fields.get('title'),
                     body=blog_fields.get('body'),
                     preview=blog_fields.get('preview'),
                     is_published=blog_fields.get('is_published'))
            )
        Blog.objects.bulk_create(blog_for_create)

        # Заполнение блога
        for version in Command.json_read(DATA_VERSION):
            version_fields = version.get('fields')
            version_for_create.append(
                Version(product=Product.objects.get(pk=version_fields.get('product')),
                        version_number=version_fields.get('version_number'),
                        version_name=version_fields.get('version_name'),
                        is_active=version_fields.get('is_active'))
            )
        Version.objects.bulk_create(version_for_create)
