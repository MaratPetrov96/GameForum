# Generated by Django 3.0.5 on 2022-01-09 04:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ForumApp', '0003_comment_is_reply'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='replies',
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='ForumApp.Comment'),
        ),
    ]
