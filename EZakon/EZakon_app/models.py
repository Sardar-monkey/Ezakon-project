from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from pytils.translit import slugify

class Lawyer(models.Model):
    name = models.CharField("Имя юриста", max_length=255)
    description = models.TextField("Описание юриста", default="Описание отсутствует")
    status = models.CharField("Статус юриста", default="Нету статуса", max_length=255 )
    image_url = models.URLField("Вставьте изображение", max_length=500, default='', blank=True)
    closed = models.IntegerField("Дел закрыто", default="0")
    rating = models.IntegerField("Оценка", default="0")
    com = models.IntegerField("Отзывы", default="0")
    succses = models.IntegerField("Успешно закрыто дел", default=0)
    stazh = models.IntegerField("Стаж работы", default="0")
    phone = models.IntegerField("номер телефона")
    slug = models.SlugField(unique=True, editable=False, blank=True)
    created_at = models.DateTimeField(verbose_name="Время создания", default=datetime.now)

    class Meta:
        verbose_name = "Резюме юриста"
        verbose_name_plural = "Резюме юристов"

    def __str__(self):
        return f"{self.pk} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Comment(models.Model):
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField("Текст отзыва")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']

    def __str__(self):
        return f'Отзыв от {self.author.username} о юристе {self.lawyer.name}'
