# Generated by Django 4.2 on 2023-04-16 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0007_alter_agriculturebasics_publisheddatetime_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='role',
            field=models.TextField(default='', max_length=100),
        ),
    ]
