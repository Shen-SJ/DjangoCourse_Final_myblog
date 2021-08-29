from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from mysite import models
from collections import OrderedDict


# Create your views here.
def recent_posts(number=5):
    recent_articles = models.Articles.objects.filter(visible=True).order_by('-pub_date')[0:number]
    return recent_articles


def tags_cloud():
    # determine all tags frequency
    tag_freq = {}
    for tag in models.Tags.objects.all():
        tag_freq[tag.name] = len(models.Articles.objects.filter(tags=tag))
    most_freq = max(tag_freq.values())
    interval = (most_freq - 1) / 6

    # classified depends on the tag frequency
    tags_class = OrderedDict()
    for tag in models.Tags.objects.all().order_by('name'):
        tag_class = None
        if most_freq == len(models.Articles.objects.filter(tags=tag)):
            tag_class = 0
        elif (most_freq > len(models.Articles.objects.filter(tags=tag))) and \
             (len(models.Articles.objects.filter(tags=tag)) >= most_freq-interval):
            tag_class = 1
        elif (most_freq-interval > len(models.Articles.objects.filter(tags=tag))) and \
             (len(models.Articles.objects.filter(tags=tag)) >= most_freq-interval*2):
            tag_class = 2
        elif (most_freq-interval*2 > len(models.Articles.objects.filter(tags=tag))) and \
             (len(models.Articles.objects.filter(tags=tag)) >= most_freq-interval*3):
            tag_class = 3
        elif (most_freq-interval*3 > len(models.Articles.objects.filter(tags=tag))) and \
             (len(models.Articles.objects.filter(tags=tag)) >= most_freq-interval*4):
            tag_class = 4
        elif (most_freq-interval*4 > len(models.Articles.objects.filter(tags=tag))) and \
             (len(models.Articles.objects.filter(tags=tag)) >= most_freq-interval*5):
            tag_class = 5
        elif (most_freq-interval*5 > len(models.Articles.objects.filter(tags=tag))) and \
             (len(models.Articles.objects.filter(tags=tag)) >= 1):
            tag_class = 6
        elif len(models.Articles.objects.filter(tags=tag)) == 0:
            continue
        tags_class[tag.name] = tag_class
    return tags_class


def index(request):
    # show the recent posts and tags cloud in sidebar
    recent_articles = recent_posts()
    tags_classified = tags_cloud()

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


def aboutme(request):
    # show the recent posts and tags cloud in sidebar
    recent_articles = recent_posts()
    tags_classified = tags_cloud()
    return render(request, 'aboutme.html', locals())


def article_page(request, slug):
    # show the recent posts and tags cloud in sidebar
    recent_articles = recent_posts()
    tags_classified = tags_cloud()
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
        msg = '很抱歉，您所選取的文章不存在，請回到首頁'
        return render(request, '404.html', locals())
    return render(request, 'article.html', locals())
