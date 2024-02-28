from django.contrib import admin
from django.utils.html import format_html
from mysite import models


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'pub_date', 'visible', 'series')


class WeddingPhotosAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'order', 'large_url', 'medium_url', 'small_url', 'comment', 'establish_date')
    readonly_fields = ('image_tag',)


admin.site.register(models.Articles, ArticleAdmin)
admin.site.register(models.Tags)
admin.site.register(models.Series)
admin.site.register(models.WeddingPhotos, WeddingPhotosAdmin)
