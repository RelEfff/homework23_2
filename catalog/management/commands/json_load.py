import json
from django.conf import settings
from django.core.management import BaseCommand
from catalog.models import Product, Category

FIXTURES_PATH = settings.BASE_DIR.joinpath('catalog.json')


class Command(BaseCommand):

    @staticmethod
    def json_read():
        # Открываем файл с фикстурами категорий и загружаем данные в формате
        # JSON
        with open(FIXTURES_PATH, 'r', encoding='utf-8') as file:
            categories = json.load(file)
        return categories

    def handle(self, *args, **options):
        # Удаляем все продукты из базы данных
        Product.objects.all().delete()
        # Удаляем все категории из базы данных
        Category.objects.all().delete()

        # Создаем списки для хранения объектов категорий и продуктов
        product_for_create = []
        category_for_create = []

        # Обходим все значения категорий из фикстуры для получения информации
        # об одном объекте
        for category in Command.json_read():
            if category['model'] == 'catalog.category':
                category_for_create.append(
                    Category(
                        name=category['fields']['name'],
                        description=category['fields']['description'],
                        pk=category['pk'],
                    )
                )

        # Создаем объекты категорий в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)

        # Обходим все значения продуктов из фикстуры для получения информации
        # об одном объекте
        for product in Command.json_read():
            if product['model'] == 'catalog.product':
                product_for_create.append(
                    Product(
                        name=product['fields']['name'],
                        description=product['fields']['description'],
                        price=product['fields']['price'],
                        image=product['fields']['image'],
                        created_at=product['fields']['created_at'],
                        updated_at=product['fields']['updated_at'],
                        category=Category.objects.get(pk=product['fields']['category']),

                    )
                )

        # Создаем объекты продуктов в базе с помощью метода bulk_create()
        Product.objects.bulk_create(product_for_create)
