# Generated by Django 3.2.5 on 2024-02-25 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0008_auto_20240225_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weddingphotos',
            name='comment',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
