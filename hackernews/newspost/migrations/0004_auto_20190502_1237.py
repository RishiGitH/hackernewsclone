# Generated by Django 2.2 on 2019-05-02 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newspost', '0003_auto_20190502_0929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='post_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commeted_post', to='newspost.Post'),
        ),
    ]
