# Generated by Django 3.0 on 2021-12-14 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Item', '0007_auto_20211210_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
