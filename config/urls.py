from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # Public homepage (news)
    path('', include('news.urls')),

    # API urls
    path('api/', include('mqqt_web.urls')),


    # Control panel and broker management (behind login)
    path('control/', include('dashboard.urls')),     # e.g. /control/
    # path('', include('dashboard.urls')),
    
                                    # Auth part
    path('login/',  auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', include('dashboard.urls')),  
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
