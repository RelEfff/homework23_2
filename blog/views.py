from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from blog.models import Blog
from blog.services import send_email


class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'content', 'preview_image')
    success_url = reverse_lazy('blog:blog_list')

    def form_valid(self, form):
        if form.is_valid():
            blog = form.save(commit=False)
            blog.slug = slugify(blog.title)
            blog.save()
        return super().form_valid(form)


class BlogListView(ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset().filter(is_published=True)


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.is_published:
            self.object.view_counter += 1
            if self.object.view_counter == 100:
                send_email(self.object)
            self.object.save()
            return self.object
        else:
            return None


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'content', 'preview_image')

    def get_success_url(self):
        return reverse('blog:blog_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        if form.is_valid():
            blog = form.save(commit=False)
            blog.slug = slugify(blog.title)
            blog.save()
        return super().form_valid(form)


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog_list')
