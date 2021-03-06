# Generated by Django 3.0 on 2021-08-24 11:34

import Item.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Item', '0003_auto_20210824_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(default='default/default-product.png', help_text='Maximum file size allowed is 2Mb', upload_to='item', validators=[Item.models.validate_image]),
        ),
    ]
