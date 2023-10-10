# Generated by Django 4.1.7 on 2023-08-31 09:58

from django.db import migrations, models
import django_cryptography.fields
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_alter_notepaluser_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="notepaluser",
            name="api_key",
            field=django_cryptography.fields.encrypt(
                models.CharField(default=uuid.uuid4, max_length=255)
            ),
        ),
    ]