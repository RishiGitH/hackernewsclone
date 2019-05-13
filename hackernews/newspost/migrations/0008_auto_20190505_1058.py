# Generated by Django 2.2 on 2019-05-05 10:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newspost', '0007_auto_20190505_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_upvote',
            field=models.ManyToManyField(blank=True, related_name='comment_upvotes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_upvote',
            field=models.ManyToManyField(blank=True, related_name='post_upvotes', to=settings.AUTH_USER_MODEL),
        ),
    ]