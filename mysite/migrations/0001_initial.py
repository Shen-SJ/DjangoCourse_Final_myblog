# Generated by Django 3.2.5 on 2021-08-28 15:32

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.CharField(max_length=200)),
                ('abstract', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('visible', models.BooleanField(default=False)),
                ('body', ckeditor.fields.RichTextField()),
                ('series', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mysite.series')),
                ('tags', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.tags')),
            ],
            options={
                'ordering': ('pub_date',),
            },
        ),
    ]
