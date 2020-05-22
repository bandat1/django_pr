from django.contrib import admin
from .models import Post # импортировали (включили) модель Post, которую определили в models.py

admin.site.register(Post) # Чтобы наша модель стала доступна на странице администрирования