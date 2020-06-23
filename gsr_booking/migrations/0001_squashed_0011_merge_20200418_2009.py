# Generated by Django 3.0.4 on 2020-04-19 01:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    replaces = [
        ("gsr_booking", "0001_initial"),
        ("gsr_booking", "0002_auto_20191208_1251"),
        ("gsr_booking", "0003_auto_20191208_2144"),
        ("gsr_booking", "0004_auto_20191225_1527"),
        ("gsr_booking", "0005_usersearchindex"),
        ("gsr_booking", "0006_gsrbookingcredentials"),
        ("gsr_booking", "0007_auto_20200202_1159"),
        ("gsr_booking", "0008_auto_20200202_1218"),
        ("gsr_booking", "0009_auto_20200202_1232"),
        ("gsr_booking", "0010_auto_20200202_1243"),
        ("gsr_booking", "0006_auto_20200207_2126"),
        ("gsr_booking", "0011_merge_20200418_2009"),
    ]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Group",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("color", models.CharField(max_length=8)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="GroupMembership",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("accepted", models.BooleanField(default=False)),
                ("type", models.CharField(choices=[("A", "Admin"), ("M", "M")], max_length=10)),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="gsr_booking.Group"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="memberships",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("notifications", models.BooleanField(default=True)),
                ("pennkey_allow", models.BooleanField(default=False)),
                ("username", models.CharField(blank=True, default=None, max_length=127, null=True)),
            ],
            options={"verbose_name": "Group Membership",},
        ),
        migrations.AddField(
            model_name="group",
            name="members",
            field=models.ManyToManyField(
                related_name="booking_groups",
                through="gsr_booking.GroupMembership",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="group",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="group", name="color", field=models.CharField(max_length=255),
        ),
        migrations.CreateModel(
            name="UserSearchIndex",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("full_name", models.CharField(db_index=True, max_length=255)),
                ("pennkey", models.CharField(db_index=True, max_length=255)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="GSRBookingCredentials",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "session_id",
                    models.CharField(
                        max_length=50, null=True, unique=True, verbose_name="Session ID"
                    ),
                ),
                (
                    "expiration_date",
                    models.DateTimeField(null=True, verbose_name="Session ID expiration date"),
                ),
                (
                    "email",
                    models.CharField(
                        max_length=255, null=True, unique=True, verbose_name="school email"
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "date_updated",
                    models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
                ),
            ],
            options={
                "verbose_name": "GSR Booking Credentials",
                "verbose_name_plural": "GSR Booking Credentials",
            },
        ),
        migrations.AlterField(
            model_name="groupmembership",
            name="group",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="memberships",
                to="gsr_booking.Group",
            ),
        ),
        migrations.AlterField(
            model_name="groupmembership",
            name="type",
            field=models.CharField(choices=[("A", "Admin"), ("M", "Member")], max_length=10),
        ),
    ]