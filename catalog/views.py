from django.shortcuts import render

from catalog.models import Product


def product_list(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'catalog/product_list.html', context=context)


def contacts(request):
    return render(request, 'contacts.html')


def product_detail(request, pk):
    product = Product.objects.filter(pk=pk).first()
    context = {'product': product}
    return render(request, 'catalog/product_detail.html', context=context)
