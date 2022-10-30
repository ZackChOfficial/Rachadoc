# Generated by Django 4.1.1 on 2022-10-30 13:34

import accounts.managers
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("clinic", "__first__"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(blank=True, null=True, verbose_name="last login"),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(blank=True, max_length=150, verbose_name="first name"),
                ),
                (
                    "last_name",
                    models.CharField(blank=True, max_length=150, verbose_name="last name"),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(default=django.utils.timezone.now, verbose_name="date joined"),
                ),
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
                    "email",
                    models.EmailField(max_length=254, unique=True, verbose_name="address email"),
                ),
                (
                    "phone_number",
                    models.CharField(max_length=255, verbose_name="numéro de téléphone"),
                ),
                (
                    "cnie",
                    models.CharField(
                        max_length=255,
                        verbose_name="carte nationale d'identité électronique",
                    ),
                ),
                (
                    "date_of_birth",
                    models.DateField(null=True, verbose_name="date de naissance"),
                ),
                (
                    "gender",
                    models.IntegerField(
                        choices=[(1, "Inconnu"), (2, "Homme"), (3, "Femme")],
                        default=1,
                        verbose_name="date de naissance",
                    ),
                ),
                ("picture", models.URLField(verbose_name="photo de profil")),
                (
                    "email_verified",
                    models.BooleanField(default=False, verbose_name="email verifier"),
                ),
                (
                    "phone_verified",
                    models.BooleanField(default=False, verbose_name="numéro de téléphone verifier"),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", accounts.managers.BaseUserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Doctor",
            fields=[
                (
                    "user_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "description",
                    models.CharField(max_length=4096, verbose_name="description"),
                ),
                ("INP", models.CharField(max_length=127, verbose_name="INP")),
                (
                    "appointement_duration",
                    models.IntegerField(default=15, verbose_name="Durée du rendez-vous"),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            bases=("accounts.user",),
        ),
        migrations.CreateModel(
            name="Patient",
            fields=[
                (
                    "user_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "city",
                    models.CharField(max_length=255, verbose_name="ville de residence"),
                ),
                ("address", models.CharField(max_length=2048, verbose_name="address")),
                (
                    "CIVIL_STATUS",
                    models.IntegerField(
                        choices=[(1, "Inconnu"), (2, "Marié"), (3, "Célibataire")],
                        default=1,
                        verbose_name="État civil",
                    ),
                ),
                (
                    "insurance",
                    models.IntegerField(choices=[(1, "Inconnu")], default=1, verbose_name="Mutuelle"),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            bases=("accounts.user",),
        ),
        migrations.CreateModel(
            name="Receptionist",
            fields=[
                (
                    "user_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "clinic",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="clinic.clinic"),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            bases=("accounts.user",),
        ),
    ]
