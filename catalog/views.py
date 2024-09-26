from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, TemplateView, DetailView, DeleteView, CreateView, UpdateView

from catalog.forms import ProductForm, VersionForm, ProductModerationForm
from catalog.models import Product, Version


class ContactsTemplateView(TemplateView):
    template_name = 'contacts.html'


class ProductListView(LoginRequiredMixin, ListView):
    model = Product

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.has_perm('catalog.view_product'):
            return Product.objects.all()
        return Product.objects.filter(is_published=True).all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for obj in context['object_list']:
            obj.active_version = obj.versions.filter(
                is_active=True).first() if obj.versions.filter(
                is_active=True).first() else "Активная версия не найдена"
        return context


class PersonalProductListView(LoginRequiredMixin, ListView):
    model = Product

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.has_perm('catalog.view_product'):
            return Product.objects.all()
        return Product.objects.filter(owner=self.request.user).all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for obj in context['object_list']:
            obj.active_version = obj.versions.filter(
                is_active=True).first() if obj.versions.filter(
                is_active=True).first() else "Активная версия не найдена"
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('catalog:product_list')

    def form_valid(self, form):
        product = form.save(commit=False)
        product.owner = self.request.user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if type(context['form']) == ProductForm:
            ProductFormset = inlineformset_factory(Product, Version, VersionForm,
                                                   extra=1)
            if self.request.method == 'POST':
                context['formset'] = ProductFormset(self.request.POST,
                                                    instance=self.object)
            else:
                context['formset'] = ProductFormset(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context.get('formset')
        if formset:
            if form.is_valid() and formset.is_valid():
                active_version = 0
                for i in formset.forms:
                    if i.cleaned_data.get('is_active'):
                        active_version += 1
                    if active_version > 1:
                        form.add_error(None,
                                       'Вы можете выбрать только одну активную версию')
                        return self.form_invalid(form)
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        elif form.is_valid():
            form.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(
                self.get_context_data(form=form, formset=formset))

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return ProductForm
        if user.has_perms(
                ['catalog.product_set_published_status', 'catalog.product_change_description',
                 'catalog.product_change_category']):
            return ProductModerationForm
        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product

    def get_success_url(self, *args, **kwargs):
        return reverse('catalog:product_list')
