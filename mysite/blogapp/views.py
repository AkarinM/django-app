from django.shortcuts import render
from django.views.generic import ListView
from .models import Article

class ArticlesListView(ListView):
    template_name = 'blogapp/articles_list.html'
    queryset = Article.objects.select_related('author', 'category').prefetch_related('tags').defer('content').all()
    context_object_name = 'articles'
