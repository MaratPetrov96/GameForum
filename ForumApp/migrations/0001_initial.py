# Generated by Django 3.0.5 on 2021-12-08 12:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=45, verbose_name='Жанр')),
            ],
        ),
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=90, verbose_name='Название')),
                ('descr', models.TextField(verbose_name='Описание')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('tags', models.ManyToManyField(related_name='ideas', to='ForumApp.Tag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ideas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Содержание')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('idea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comms', to='ForumApp.Idea')),
                ('replies', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ForumApp.Comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comms', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
