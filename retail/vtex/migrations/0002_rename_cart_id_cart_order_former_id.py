# Generated by Django 5.1.1 on 2025-01-22 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("vtex", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="cart",
            old_name="cart_id",
            new_name="order_former_id",
        ),
    ]
