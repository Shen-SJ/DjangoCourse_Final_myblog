# Generated by Django 3.2.5 on 2021-08-28 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0002_alter_articles_series'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articles',
            name='tags',
        ),
        migrations.AddField(
            model_name='articles',
            name='tags',
            field=models.ManyToManyField(to='mysite.Tags'),
        ),
    ]
