# Generated by Django 2.2 on 2019-05-07 12:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('newspost', '0013_auto_20190507_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_upvote',
            field=models.ManyToManyField(blank=True, related_name='comment_upvotes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='comment',
            name='comment_upvotes',
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_upvotes',
            field=models.IntegerField(default=0),
        ),
    ]
