from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from ckeditor.fields import RichTextField


# Create your models here.
class Tags(models.Model):
    name = models.CharField(unique=True, max_length=100)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Series(models.Model):
    name = models.CharField(unique=True, max_length=200)

    def __str__(self):
        return self.name


class Articles(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(unique=True, max_length=200)
    abstract = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tags)
    visible = models.BooleanField(default=False)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, null=True, blank=True)
    body = RichTextField()

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return self.title
    

class WeddingPhotos(models.Model):
    order = models.IntegerField()
    large_url = models.CharField(max_length=200)
    medium_url = models.CharField(max_length=200)
    small_url = models.CharField(max_length=200)
    comment = models.CharField(max_length=200, blank=True)
    establish_date = models.DateTimeField(default=timezone.now)
    
    def image_tag(self):
        # used in the admin site model as a "thumbnail"
        return mark_safe('<img src="{}" width="150" height="150" />'.format(self.small_url) )
    image_tag.short_description = 'Image'  

    class Meta:
        ordering = ('order',)

