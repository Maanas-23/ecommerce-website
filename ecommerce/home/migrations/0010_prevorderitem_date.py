# Generated by Django 4.0.1 on 2022-03-15 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_remove_prevorderitem_cart_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='prevorderitem',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
