# Generated by Django 2.2.7 on 2019-12-08 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_groupmembership_pennkey_allow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='color',
            field=models.CharField(max_length=255),
        ),
    ]
