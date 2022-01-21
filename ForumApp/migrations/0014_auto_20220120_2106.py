# Generated by Django 3.0.5 on 2022-01-20 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ForumApp', '0013_tag_subscribers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(verbose_name='Content'),
        ),
        migrations.AlterField(
            model_name='idea',
            name='descr',
            field=models.TextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='idea',
            name='title',
            field=models.CharField(max_length=90, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='title',
            field=models.CharField(max_length=45, verbose_name='Tag'),
        ),
    ]