# Generated by Django 4.2 on 2023-05-20 11:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("clinic", "0001_initial"),
        ("accounts", "0003_alter_doctor_managers_alter_patient_managers_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="patient",
            name="clinics",
            field=models.ManyToManyField(related_name="patients", to="clinic.clinic"),
        ),
    ]
