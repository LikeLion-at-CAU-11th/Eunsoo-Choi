# Generated by Django 4.1.7 on 2023-08-01 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(null=True, upload_to='', verbose_name='썸네일'),
        ),
    ]
