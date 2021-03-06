# Generated by Django 3.2.4 on 2021-08-16 12:32

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='DOB',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.TextField(blank=True, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='image',
            field=app.models.ImageField(blank=True, null=True, upload_to='users'),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]
