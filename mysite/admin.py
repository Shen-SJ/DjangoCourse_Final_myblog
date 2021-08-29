from django.contrib import admin
from mysite import models


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'pub_date', 'visible', 'series')


admin.site.register(models.Articles, ArticleAdmin)
admin.site.register(models.Tags)
admin.site.register(models.Series)
