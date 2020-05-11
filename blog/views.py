from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import PostForm

"""Точка перед models означает текущую директорию или текущее приложение. 
Поскольку views.py и models.py находятся в одной директории, мы можем использовать точку . и имя файла 
(без расширения .py). Затем мы импортируем модель (Post)."""

from .models import Post

"""мы создали функцию (def) с именем post_list, которая принимает request в качестве аргумента и возвращает (return) 
 результат работы функции render, которая уже соберёт наш шаблон страницы blog/post_list.html.
 Предназначены представления: соединять между собой модели и шаблоны."""

def post_list(request): # post_list displays only published blog posts (those with non-empty published_date)
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    """Последний параметр, который выглядит как {}, — это место, куда мы можем добавить что-нибудь для использования 
    в шаблоне. Мы должны задавать имена передаваемым шаблону вещам (прямо сейчас мы остановимся на 'posts' """

    return render(request, 'blog/post_list.html', {'posts': posts})

"""создали шаблон URL под названием post_detail, который ссылался на представление под названием views.post_detail. 
Это значит, что Django ожидает найти функцию-представление с названием post_detail в blog/views.py"""

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

"""в представлении view нам нужно обработать две разные ситуации. 
Первая: когда мы только зашли на страницу и хотим получить пустую форму. 
Вторая: когда мы возвращаемся к представлению со всей информацией, которую мы ввели в форму."""

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST) # Если method — POST, тогда мы хотим построить PostForm с данными из формы
        if form.is_valid(): # проверим, корректна ли форма (все ли необходимые поля заполнены и не отправлено ли некорректных значений)
            post = form.save(commit=False) # commit=False означает, что мы пока не хотим сохранять модель Post — сначала нужно добавить автора
            post.author = request.user
            #post.published_date = timezone.now() # проверяем, допустимо ли содержимое формы
            post.save() # сохранит изменения (после добавления автора), и новая запись будет создана

            # post_detail — это имя представления, которое нам необходимо. Помнишь, что это представление требует переменную pk?
            # Чтобы передать её представлению, мы используем аргумент pk=post.pk, где post — это новая запись в блоге!
            return redirect('post_detail', pk=post.pk) # переадресация на страницу post_detail для созданной записи
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

# мы передаём параметр pk из URL-адреса. Кроме того, мы получаем модель Post для редактирования при помощи get_object_or_404(Post, pk=pk)
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk) # передаём экземпляр post в качестве instance форме и при сохранении
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post) # когда мы открываем форму для редактирования
    return render(request, 'blog/post_edit.html', {'form': form})


def post_draft_list(request):

    # we take only unpublished posts (published_date__isnull=True) and order them by created_date
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)
