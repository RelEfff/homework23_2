from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ContactsTemplateView, ProductDetailView, ProductCreateView, \
    ProductDeleteView, ProductUpdateView, PersonalProductListView, CategoryListView

app_name = CatalogConfig.name

urlpatterns = [
    path('', CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>/', ProductListView.as_view(), name='product_list'),
    path('personal_product_list/', PersonalProductListView.as_view(), name='personal_product_list'),
    path('contacts/', ContactsTemplateView.as_view(), name='contacts'),
    path('product_detail/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),
    path('product_create/', ProductCreateView.as_view(), name='product_create'),
    path('product_delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('product_update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
]
