# Generated by Django 5.0.7 on 2024-07-31 18:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("features", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="featureversion",
            name="brain",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="feature_version",
                to="features.brain",
            ),
        ),
    ]
