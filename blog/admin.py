from django.contrib import admin
from blog.models import Article
# Register your models here.



@admin.register(Article)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'create_date', 'is_published')
    search_fields = ('title', 'text',)
