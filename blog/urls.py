from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import ArticleCreateView, ArticleListView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('blog', ArticleListView.as_view(), name="blog"),
    path('blog/create', ArticleCreateView.as_view(), name="create_article"),
    path('article/<int:pk>', ArticleDetailView.as_view(), name="view_article"),
    path('edit/<int:pk>', ArticleUpdateView.as_view(), name="update_article"),
    path('delete/<int:pk>', ArticleDeleteView.as_view(), name="delete_article"),
]