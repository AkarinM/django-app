from django.db import models


class Author(models.Model):
    """
    Представляет автора статьи
    """
    name = models.CharField(max_length=40,)
    bio = models.TextField()


class Category(models.Model):
    """
    Категория статьи
    """
    name = models.CharField(max_length=40)


class Tag(models.Model):
    """
    Тег, который можно назначить статье
    """
    name = models.CharField(max_length=20)


class Article(models.Model):
    """
    Статья
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories')
    tags = models.ManyToManyField(Tag, related_name='tag_articles')
