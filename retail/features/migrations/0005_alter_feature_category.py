# Generated by Django 5.0.7 on 2024-08-01 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("features", "0004_rename_names_brain_actions_brain_instructions_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feature",
            name="category",
            field=models.CharField(
                choices=[("ATIVO", "Ativo"), ("PASSIVO", "Passivo")],
                default="Ativo",
                max_length=256,
            ),
        ),
    ]
