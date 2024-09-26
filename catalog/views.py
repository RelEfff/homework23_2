from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, TemplateView, DetailView, DeleteView, CreateView

from catalog.models import Product


class ProductListView(ListView):
    model = Product


class ContactsTemplateView(TemplateView):
    template_name = 'contacts.html'


class ProductDetailView(DetailView):
    model = Product


# class ProductCreateView(CreateView):
#     model = Product
#
#     def get_success_url(self):
#         return reverse('catalog:product_list')
#
#
# class ProductDeleteView(DeleteView):
#     model = Product
#     success_url = reverse('catalog:product_list')
