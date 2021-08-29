from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from mysite import models


# Create your views here.
def recent_posts(number=5):
    recent_articles = models.Articles.objects.filter(visible=True).order_by('-pub_date')[0:number]
    return recent_articles


def index(request):
    # show the recent posts in sidebar
    recent_articles = recent_posts()

    # list all of the articles in the body
    articles = models.Articles.objects.filter(visible=True).order_by('-pub_date')
    articles = [
        {'title': ar.title,
         'abstract': ar.abstract,
         'slug': ar.slug,
         'isotime': timezone.make_naive(ar.pub_date).isoformat(),
         'time': timezone.make_naive(ar.pub_date).strftime("%a %d %m月 %YT%H:%M:%S"),
         'tags': ar.tags.all(),
         } for ar in articles
    ]
    return render(request, 'index.html', locals())


def article_page(request, slug):
    # show the recent posts in sidebar
    recent_articles = recent_posts()
    try:
        article = models.Articles.objects.get(slug=slug)
        article = {
            'title': article.title,
            'abstract': article.abstract,
            'slug': article.slug,
            'isotime': timezone.make_naive(article.pub_date).isoformat(),
            'time': timezone.make_naive(article.pub_date).strftime("%a %d %m月 %YT%H:%M:%S"),
            'tags': article.tags.all(),
            'visible': article.visible,
            'series': article.series,
            'body': article.body
        }
    except:
        pass    # 應該要顯示文章不存在的畫面
    return render(request, 'article.html', locals())
