# Generated by Django 4.2.2 on 2023-06-17 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctionsHub', '0004_cart_total_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='items',
            new_name='item',
        ),
    ]