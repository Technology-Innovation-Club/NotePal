# Generated by Django 4.1.7 on 2023-10-08 11:09

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_notepaluser_api_key"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notepaluser",
            name="api_key",
            field=django_cryptography.fields.encrypt(
                models.CharField(default="", max_length=255)
            ),
        ),
    ]
