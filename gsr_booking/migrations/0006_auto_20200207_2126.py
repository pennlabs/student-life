# Generated by Django 3.0.2 on 2020-02-08 02:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gsr_booking", "0005_usersearchindex"),
    ]

    operations = [
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
