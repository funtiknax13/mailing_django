from django.db import models

from users.models import User

NULLABLE = {'null': True, 'blank': True}


# Create your models here.
class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Автор', **NULLABLE)
    title = models.CharField(max_length=300, verbose_name='Заголовок')
    slug = models.CharField(max_length=300, verbose_name='Slug')
    text = models.TextField(verbose_name='Содержимое')
    image = models.ImageField(upload_to='blog/', **NULLABLE, verbose_name='Превью')
    create_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    is_published = models.BooleanField(default=True, verbose_name='Статус публикации')
    view_count = models.IntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
