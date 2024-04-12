import json
import pathlib

from django.core.management import BaseCommand
from django.db import connection

from catalog.models import Category, Product

ROOT = pathlib.Path(__file__).parent.parent.parent.parent
DATA_CATEGORY = pathlib.Path(ROOT, 'data', 'category.json')
DATA_PRODUCT = pathlib.Path(ROOT, 'data', 'product.json')


class Command(BaseCommand):

    @staticmethod
    def json_read_categories() -> list:
        # Здесь мы получаем данные из фикстур с категориями
        with open(DATA_CATEGORY, encoding="utf-8") as file:
            file_info = json.load(file)
        return [info for info in file_info]

    @staticmethod
    def json_read_products() -> list:
        # Здесь мы получаем данные из фикстур с продуктами
        with open(DATA_PRODUCT, encoding="utf-8") as file:
            file_info = json.load(file)
        return [info for info in file_info]

    def handle(self, *args, **options):
        # Очистка базы данных перед заполнением
        Category.objects.all().delete()
        Product.objects.all().delete()

        category_for_create = []
        product_for_create = []

        with connection.cursor() as cursor:
            cursor.execute(
                "TRUNCATE TABLE catalog_category, catalog_product RESTART IDENTITY CASCADE;")

        # Заполнение категорий
        for category in Command.json_read_categories():
            category_fields = category.get('fields')
            category_for_create.append(
                Category(category_name=category_fields.get('category_name'),
                         category_description=category_fields.get('category_description'))
            )

        Category.objects.bulk_create(category_for_create)

        # Заполнение продуктов
        for product in Command.json_read_products():
            product_fields = product.get('fields')
            product_for_create.append(
                Product(products_name=product_fields.get('products_name'),
                        category=Category.objects.get(pk=product_fields.get('category')))
            )
        Product.objects.bulk_create(product_for_create)
