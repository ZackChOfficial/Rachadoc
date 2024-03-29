# Generated by Django 4.1.7 on 2023-03-04 23:19

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AppointementNotification",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (2, "Livré"),
                            (4, "Échec de la livraison"),
                            (3, "Désengagement"),
                            (1, "Programmé"),
                        ]
                    ),
                ),
                ("channel", models.IntegerField(choices=[(1, "Email"), (2, "SMS")])),
                ("scheduled_at", models.DateTimeField()),
                ("delivered_at", models.DateTimeField(blank=True, null=True)),
                ("extra_data", models.JSONField(blank=True, null=True)),
                ("target_id", models.CharField(max_length=4096)),
                (
                    "appointement",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="_appointement_notifs",
                        to="events.appointement",
                    ),
                ),
            ],
            options={
                "unique_together": {("appointement", "channel", "scheduled_at")},
            },
        ),
    ]
