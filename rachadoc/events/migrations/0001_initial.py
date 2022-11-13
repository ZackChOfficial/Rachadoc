# Generated by Django 4.1.1 on 2022-11-06 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
        ("clinic", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
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
                ("from_date", models.DateTimeField(verbose_name="date de début")),
                ("to_date", models.DateTimeField(verbose_name="date de fin")),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (1, "Inconnu"),
                            (2, "Prochain"),
                            (3, "En cours"),
                            (4, "Terminé"),
                            (5, "Annulé"),
                        ],
                        default=1,
                        verbose_name="Status",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Personal",
            fields=[
                (
                    "event_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="events.event",
                    ),
                ),
                ("note", models.CharField(max_length=2048, verbose_name="note")),
                (
                    "doctor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.doctor",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("events.event",),
        ),
        migrations.CreateModel(
            name="Appointement",
            fields=[
                (
                    "event_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="events.event",
                    ),
                ),
                (
                    "note_pre_appointement",
                    models.CharField(max_length=2048, verbose_name="note pré rendez-vous "),
                ),
                (
                    "note_post_appointement",
                    models.CharField(max_length=2048, verbose_name="note après le rendez-vous"),
                ),
                (
                    "clinic",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="clinic.clinic"),
                ),
                (
                    "doctor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.doctor",
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.patient",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("events.event",),
        ),
    ]
