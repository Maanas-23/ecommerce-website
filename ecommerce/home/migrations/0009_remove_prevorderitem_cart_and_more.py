# Generated by Django 4.0.1 on 2022-03-15 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_remove_cartitem_checkout_prevorderitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prevorderitem',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='prevorderitem',
            name='checkout',
        ),
        migrations.AddField(
            model_name='prevorderitem',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.customer'),
        ),
        migrations.AddField(
            model_name='prevorderitem',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]
