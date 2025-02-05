# Generated by Django 5.1.1 on 2024-12-30 14:18

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("features", "0016_integratedfeature_config"),
        ("projects", "0004_project_vtex_account"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("cart_id", models.CharField(blank=True, null=True)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("created", "Created"),
                            ("purchased", "Purchased"),
                            ("delivered_success", "Delivered Success"),
                            ("delivered_error", "Delivered Error"),
                            ("empty", "Empty"),
                        ],
                        default="created",
                        max_length=20,
                        verbose_name="Status of Cart",
                    ),
                ),
                ("phone_number", models.CharField(max_length=15)),
                ("config", models.JSONField(default=dict)),
                ("abandoned", models.BooleanField(default=False)),
                ("error_message", models.TextField(blank=True, null=True)),
                (
                    "integrated_feature",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="carts_by_feature",
                        to="features.integratedfeature",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="carts_by_project",
                        to="projects.project",
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["project", "status"],
                        name="vtex_cart_project_da4d1d_idx",
                    )
                ],
            },
        ),
    ]
