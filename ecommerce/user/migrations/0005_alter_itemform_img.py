# Generated by Django 4.0.1 on 2022-03-15 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_itemform_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemform',
            name='img',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
