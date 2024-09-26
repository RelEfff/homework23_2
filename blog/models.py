from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=255, verbose_name='заголовок')
    slug = models.CharField(max_length=300, verbose_name='slug')
    content = models.TextField(verbose_name='содержание')
    preview_image = models.ImageField(null=True, blank=True,
                                      verbose_name='изображение для предпросмотра')
    created_at = models.DateTimeField(verbose_name='Дата создания статьи',
                                      auto_now_add=True, editable=False)
    is_published = models.BooleanField(default=False,
                                       verbose_name='опубликовано',
                                       help_text='Опубликовано')
    view_counter = models.PositiveIntegerField(default=0, editable=False,
                                               verbose_name='Количество просмотров')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
