from django.contrib import admin
from .models import NewsItem

@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'content','created_at','updated_at')
    list_filter = ('title','created_at','content')
    search_fields = ('title', 'content')
    list_display_links = ('title', 'content','created_at','updated_at')
