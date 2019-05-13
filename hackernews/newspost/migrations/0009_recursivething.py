# Generated by Django 2.2 on 2019-05-05 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newspost', '0008_auto_20190505_1058'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecursiveThing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='newspost.RecursiveThing')),
            ],
        ),
    ]