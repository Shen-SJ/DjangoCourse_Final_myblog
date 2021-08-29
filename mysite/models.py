from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField


# Create your models here.
class Tags(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Series(models.Model):
    name = models.CharField(max_length=200)


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
