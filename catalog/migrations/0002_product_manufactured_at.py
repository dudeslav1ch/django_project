# Generated by Django 5.0.4 on 2024-04-11 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='manufactured_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата производства продукта'),
        ),
    ]
