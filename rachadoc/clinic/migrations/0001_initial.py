# Generated by Django 4.1.7 on 2023-03-04 23:17

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import rules.contrib.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Clinic",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255, verbose_name="nom")),
                ("address", models.CharField(max_length=1024, verbose_name="addresse")),
                ("point", django.contrib.gis.db.models.fields.PointField(srid=4326)),
                (
                    "description",
                    models.CharField(max_length=4096, verbose_name="description"),
                ),
                (
                    "phone_number",
                    models.CharField(max_length=255, verbose_name="numéro de téléphone"),
                ),
                (
                    "email_address",
                    models.CharField(max_length=255, verbose_name="adresse email"),
                ),
            ],
            bases=(models.Model, rules.contrib.models.RulesModelMixin),
        ),
    ]
