# Generated by Django 5.1.1 on 2024-09-04 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Organizations_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=255),
        ),
    ]
