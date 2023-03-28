# Generated by Django 4.1.7 on 2023-03-28 21:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="appointement",
            name="note_pre_appointement",
            field=models.CharField(
                blank=True,
                max_length=2048,
                null=True,
                verbose_name="note pré rendez-vous",
            ),
        ),
    ]
