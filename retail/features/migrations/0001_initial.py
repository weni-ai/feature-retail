# Generated by Django 5.0.7 on 2024-07-31 17:59

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("projects", "__first__"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Brain",
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
                ("uuid", models.UUIDField(default=uuid.uuid4)),
            ],
        ),
        migrations.CreateModel(
            name="Feature",
            fields=[
                (
                    "create_on",
                    models.DateField(
                        auto_now_add=True,
                        verbose_name="when are created the new feature",
                    ),
                ),
                ("description", models.TextField(null=True)),
                ("name", models.CharField(max_length=256)),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="UUID",
                    ),
                ),
                ("category", models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name="FeatureVersion",
            fields=[
                ("created_at", models.DateField(auto_now_add=True)),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="UUID",
                    ),
                ),
                ("definition", models.JSONField()),
                ("parameters", models.JSONField(blank=True, null=True)),
                ("version", models.CharField(default="1.0", max_length=10)),
                (
                    "brain",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="feature_version",
                        to="features.brain",
                    ),
                ),
                (
                    "feature",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="feature_version",
                        to="features.feature",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="IntegratedFeature",
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
                ("integrated_on", models.DateField(auto_now_add=True)),
                (
                    "feature_version",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="integrated_feature",
                        to="features.featureversion",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="project",
                        to="projects.project",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="integrated_feature",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Flow",
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
                ("uuid", models.UUIDField()),
                ("flow_uuid", models.CharField(max_length=100, null=True)),
                ("name", models.CharField(max_length=256)),
                ("definition", models.JSONField()),
                (
                    "integrated_feature",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="flows",
                        to="features.integratedfeature",
                    ),
                ),
            ],
        ),
    ]
