# Generated by Django 4.0.1 on 2022-03-15 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_remove_order_item_orderitem_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='price',
            field=models.FloatField(default=1000),
        ),
    ]
