# Generated by Django 2.2.24 on 2021-06-25 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='images',
            name='title',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
