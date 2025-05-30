from django.db import models

class NewsItem(models.Model):
    title      = models.CharField(max_length=200)
    image      = models.ImageField(upload_to='news/')
    content    = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
