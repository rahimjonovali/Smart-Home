from django.views.generic import ListView
from .models import NewsItem

class HomePageView(ListView):
    model = NewsItem
    template_name = 'news/homepage.html'
    context_object_name = 'news_list'
    paginate_by = 5
