from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from pytils.translit import slugify


class Lawyer(models.Model):
    name = models.CharField("Имя юриста", max_length=255)
    description = models.TextField("Описание юриста", default="Описание отсутствует")
    status = models.CharField("Статус юриста", default="Нету статуса", max_length=255)
    image_url = models.URLField(
        "Вставьте изображение", max_length=500, default="", blank=True
    )
    closed = models.IntegerField("Дел закрыто", default="0")
    rating = models.IntegerField("Оценка", default="0")
    com = models.IntegerField("Отзывы", default="0")
    succses = models.IntegerField("Успешно закрыто дел", default=0)
    stazh = models.IntegerField("Стаж работы", default="0")
    phone = models.CharField("номер телефона", default="Номер юриста", max_length=20)
    slug = models.SlugField(unique=True, editable=False, blank=True)
    created_at = models.DateTimeField(
        verbose_name="Время создания", default=datetime.now
    )

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
    lawyer = models.ForeignKey(
        Lawyer, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField("Текст отзыва")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Отзыв от {self.author.username} о юристе {self.lawyer.name}"


class Law(models.Model):
    CATEGORY_CHOICES = [
        ("civil", "Гражданское право"),
        ("criminal", "Уголовное право"),
        ("labor", "Трудовое право"),
        ("family", "Семейное право"),
        ("admin", "Административное право"),
        ("tax", "Налоговое право"),
        ("property", "Право собственности"),
        ("constitutional", "Конституционное право"),
        ("international", "Международное право"),
        ("commercial", "Коммерческое право"),
        ("other", "Другое"),
    ]

    STATUS_CHOICES = [
        ("active", "Действующий"),
        ("archived", "Архивированный"),
        ("draft", "Черновик"),
        ("deprecated", "Устаревший"),
    ]

    title = models.CharField("Название закона", max_length=500)
    number = models.CharField("Номер закона", max_length=100, unique=True)
    date_published = models.DateField("Дата опубликования")
    date_updated = models.DateField("Дата обновления", auto_now=True)
    description = models.TextField("Краткое описание")
    full_text = models.TextField("Полный текст")
    category = models.CharField("Категория", choices=CATEGORY_CHOICES, max_length=50)
    status = models.CharField(
        "Статус", choices=STATUS_CHOICES, default="active", max_length=20
    )
    is_active = models.BooleanField("Действующий", default=True)
    slug = models.SlugField(unique=True, editable=False, blank=True)
    views_count = models.IntegerField("Количество просмотров", default=0)
    created_at = models.DateTimeField(verbose_name="Время создания", auto_now_add=True)

    class Meta:
        verbose_name = "Закон"
        verbose_name_plural = "Законы"
        ordering = ["-date_published"]
        indexes = [
            models.Index(fields=["category", "-date_published"]),
            models.Index(fields=["status", "is_active"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return f"{self.number} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def increment_views(self):
        """Увеличить счётчик просмотров"""
        self.views_count += 1
        self.save(update_fields=["views_count"])


class LawHistory(models.Model):

    law = models.ForeignKey(Law, on_delete=models.CASCADE, related_name="history")
    changed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    change_description = models.TextField("Описание изменения")
    previous_text = models.TextField("Предыдущий текст", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "История закона"
        verbose_name_plural = "Истории законов"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Изменение {self.law.title} от {self.created_at}"


class LawComment(models.Model):

    law = models.ForeignKey(Law, on_delete=models.CASCADE, related_name="law_comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField("Комментарий")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Комментарий к закону"
        verbose_name_plural = "Комментарии к законам"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Комментарий от {self.author.username} к {self.law.title}"


class FavoriteLaw(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorite_laws"
    )
    law = models.ForeignKey(Law, on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Избранный закон"
        verbose_name_plural = "Избранные законы"
        unique_together = ("user", "law")

    def __str__(self):
        return f"{self.user.username} добавил {self.law.title} в избранное"


class ChatFAQ(models.Model):
    """Часто задаваемые вопросы для чата"""
    question = models.TextField(verbose_name="Вопрос", unique=True)
    answer = models.TextField(verbose_name="Ответ")
    keywords = models.CharField(
        max_length=500, 
        verbose_name="Ключевые слова",
        help_text="Слова через запятую для поиска"
    )
    category = models.CharField(
        max_length=100,
        verbose_name="Категория",
        choices=[
            ('constitution', 'Конституция'),
            ('rights', 'Права человека'),
            ('procedure', 'Судебная процедура'),
            ('laws', 'Законы'),
            ('other', 'Прочее'),
        ],
        default='other'
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "FAQ для чата"
        verbose_name_plural = "FAQ для чата"
        ordering = ['-created_at']

    def __str__(self):
        return self.question[:50]
