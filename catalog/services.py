from django.core.cache import cache

from catalog.models import Category
from config.settings import CACHE_ENABLED


def cache_category_list():
    if CACHE_ENABLED:
        key = f'category_list'
        category_list = cache.get(key)
        if category_list is None:
            category_list = Category.objects.all()
            cache.set(key, category_list, timeout=60)
    else:
        category_list = Category.objects.all()
    return category_list


def cache_product_list_by_category(category_id):
    if CACHE_ENABLED:
        key = f'product_list_{category_id}'
        product_list = cache.get(key)
        if product_list is None:
            product_list = Category.objects.get(id=category_id).products.all()
            cache.set(key, product_list, timeout=60)
    else:
        product_list = Category.objects.get(id=category_id).products.all()
    return product_list
