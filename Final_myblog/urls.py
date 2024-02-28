"""Final_myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from mysite import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('article/<slug:slug>', views.article_page, name='article-url'),
    path('about/', views.aboutme),
    path('tags/<str:tag_name>', views.tag_article_list_page, name='tag-url'),
    path('tags/', views.tag_list_page),
    path('series/<str:series_name>', views.series_article_list_page, name='series-url'),
    path('series/', views.series_list_page),
    path('contact/', views.contact_page),
    path('captcha/', include('captcha.urls')),
    path('wedding/', views.wedding_index)
]

handler404 = "mysite.views.page_not_found_page"
