from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):

    # models.ForeignKey — ссылка на другую модель
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # так мы определяем текстовое поле с ограничением на количество символов
    title = models.CharField(max_length=200)
    # так определяется поле для неограниченно длинного текста
    text = models.TextField()
    # models.DateTimeField — дата и время
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self): # метод публикации для записи
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title # после вызова метода __str__() мы получим текст (строку) с заголовком записи