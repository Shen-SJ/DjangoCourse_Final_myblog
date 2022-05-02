from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from mysite import models, forms
from collections import OrderedDict
from django.forms.utils import ErrorList


# Create your views here.
def recent_posts(number=5):
    """Show the 5 post of recent posts in the sidebar"""
    recent_articles = models.Articles.objects.filter(visible=True).order_by('-pub_date')[0:number]
    return recent_articles


def tags_cloud():
    """Show the tags cloud in the sidebar"""
    # determine all tags frequency
    tags_freq = OrderedDict()
    for tag in models.Tags.objects.all():
        tags_freq[tag.name] = len(models.Articles.objects.filter(tags=tag))
    sorted_dict = sorted(tags_freq.items(), key=lambda x: x[1], reverse=True)
    tags_freq.clear()
    tags_freq.update(sorted_dict)

    return tags_freq


def index(request):
    """index page of web. show all of the articles."""
    # show the recent posts and tags cloud in sidebar
    recent_articles = recent_posts()
    tags_classified = tags_cloud()

    # search action
    item_name = request.GET.get('search_item')
    if item_name:
        title = 'Search'
        q1 = models.Articles.objects.filter(visible=True).filter(title__icontains=item_name)
        q2 = models.Articles.objects.filter(visible=True).filter(abstract__icontains=item_name)
        q3 = models.Articles.objects.filter(visible=True).filter(slug__icontains=item_name)
        q4 = models.Articles.objects.filter(visible=True).filter(body__icontains=item_name)
        q5_tag = models.Tags.objects.filter(name__icontains=item_name).values_list('id', flat=True)
        q5 = models.Articles.objects.filter(visible=True).filter(tags__in=q5_tag)
        q6_series = models.Series.objects.filter(name__icontains=item_name).values_list('id', flat=True)
        q6 = models.Articles.objects.filter(visible=True).filter(series__in=q6_series)
        articles = (q1 | q2 | q3 | q4 | q5 | q6).distinct()
        articles = [
            {'title': ar.title,
             'abstract': ar.abstract,
             'slug': ar.slug,
             'isotime': timezone.make_naive(ar.pub_date).isoformat(),
             'time': timezone.make_naive(ar.pub_date).strftime("%a %d %b"),
             'tags': ar.tags.all(),
             } for ar in articles
        ]
        return render(request, 'query_page.html', locals())

    # list all of the articles in the body
    articles = models.Articles.objects.filter(visible=True).order_by('-pub_date')
    articles = [
        {'title': ar.title,
         'abstract': ar.abstract,
         'slug': ar.slug,
         'isotime': timezone.make_naive(ar.pub_date).isoformat(),
         'time': timezone.make_naive(ar.pub_date).strftime("%a %d %b"),
         'tags': ar.tags.all(),
         } for ar in articles
    ]
    return render(request, 'index.html', locals())


def aboutme(request):
    """Show my information in the about page"""
    # show the recent posts and tags cloud in sidebar
    recent_articles = recent_posts()
    tags_classified = tags_cloud()
    return render(request, 'aboutme.html', locals())


def article_page(request, slug):
    """Show the article on page in each article"""
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
            'time': timezone.make_naive(article.pub_date).strftime("%a %d %b"),
            'tags': article.tags.all(),
            'visible': article.visible,
            'series': article.series,
            'body': article.body
        }
        if article['series']:
            target_series = models.Series.objects.get(name=article['series'])
            articles_series = models.Articles.objects.filter(visible=True).filter(series=target_series).order_by('title')
            article_now = models.Articles.objects.get(slug=slug)
    except:
        msg = '很抱歉，您所選取的文章不存在，請回到首頁'
        return render(request, '404.html', locals())
    return render(request, 'article.html', locals())


def tag_article_list_page(request, tag_name):
    """List the articles in specific tag"""
    # show the recent posts and tags cloud in sidebar
    recent_articles = recent_posts()
    tags_classified = tags_cloud()

    target_tag = None
    try:
        target_tag = models.Tags.objects.get(name=tag_name)
        item_name = tag_name
        title = 'Tag'
    except:
        msg = '很抱歉，您找尋的標籤不存在，請回到首頁'
        return render(request, '404.html', locals())
    articles = models.Articles.objects.filter(visible=True).filter(tags=target_tag).order_by('-pub_date')
    articles = [
        {'title': ar.title,
         'abstract': ar.abstract,
         'slug': ar.slug,
         'isotime': timezone.make_naive(ar.pub_date).isoformat(),
         'time': timezone.make_naive(ar.pub_date).strftime("%a %d %b"),
         'tags': ar.tags.all(),
         } for ar in articles
    ]
    return render(request, 'query_page.html', locals())


def series_article_list_page(request, series_name):
    """List the articles in specific Series"""
    # show the recent posts and tags cloud in sidebar
    recent_articles = recent_posts()
    tags_classified = tags_cloud()

    target_series = None
    try:
        target_series = models.Series.objects.get(name=series_name)
        item_name = series_name
        title = 'Series'
    except:
        msg = '很抱歉，您找尋的系列不存在，請回到首頁'
        return render(request, '404.html', locals())
    articles = models.Articles.objects.filter(visible=True).filter(series=target_series).order_by('-pub_date')
    articles = [
        {'title': ar.title,
         'abstract': ar.abstract,
         'slug': ar.slug,
         'isotime': timezone.make_naive(ar.pub_date).isoformat(),
         'time': timezone.make_naive(ar.pub_date).strftime("%a %d %b"),
         'tags': ar.tags.all(),
         } for ar in articles
    ]
    return render(request, 'query_page.html', locals())


def tag_list_page(request):
    """List the tags in this blog"""
    # show the recent posts and tags cloud in sidebar
    recent_articles = recent_posts()
    tags_classified = tags_cloud()

    # Count articles number for each tag
    title = "Tags"
    items_table = OrderedDict()
    for tag in models.Tags.objects.all().order_by('name'):
        items_table[tag.name] = len(models.Articles.objects.filter(visible=True).filter(tags=tag))
    return render(request, 'tags_series_list.html', locals())


def series_list_page(request):
    """List the series in this blog"""
    # show the recent posts and tags cloud in sidebar
    recent_articles = recent_posts()
    tags_classified = tags_cloud()

    # Count articles number for each series
    title = "Series"
    items_table = OrderedDict()
    for series in models.Series.objects.all().order_by('name'):
        items_table[series.name] = len(models.Articles.objects.filter(visible=True).filter(series=series))
    return render(request, 'tags_series_list.html', locals())


class DivErrorList(ErrorList):
    """Defined how to show the error message on form (especially contact form)"""
    def __str__(self):
        return self.as_ps()

    def as_ps(self):
        if not self:
            return ''
        return ''.join(['<p class="errorlist text-danger">%s</p>' % e for e in self])


def contact_page(request):
    """Show the Contact page to the reader and let them send the email to me by mailgun"""
    # show the recent posts and tags cloud in sidebar
    recent_articles = recent_posts()
    tags_classified = tags_cloud()

    if request.method == 'POST':
        form = forms.ContactForm(request.POST,
                                 # error_class=DivErrorList
                                 )
        if form.is_valid():
            message = '感謝您的來信！'
            user_name = form.cleaned_data['user_name']
            user_email = form.cleaned_data['user_email']
            user_message = form.cleaned_data['user_message']

            mail_body = u'''
            網友姓名：{}
            反應意見：如下
            {}'''.format(user_name, user_message)
            email = EmailMultiAlternatives(
                subject="來自【SSJ's Blog】網站的網友意見",
                body=mail_body,
                from_email=user_email,
                to=[' johnson840205@gmail.com '],    # 管理員(你自己)的email
                reply_to=["Helpdesk <support@example.com>"]
            )
            # email.send()
            form = forms.ContactForm()
        else:
            message = '請檢查您輸入的資訊是否正確！'
            for item_name, item_value in form._errors.items():
                print(item_name, item_value)
    else:
        form = forms.ContactForm()

    return render(request, 'contact.html', locals())


def page_not_found_page(request, exception):
    """Behavior of 404 page"""
    # show the recent posts and tags cloud in sidebar
    recent_articles = recent_posts()
    tags_classified = tags_cloud()
    return render(request, '404.html', locals(), status=404)
