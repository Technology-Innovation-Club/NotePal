# Generated by Django 4.1.7 on 2023-10-09 04:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("sessions", "0001_initial"),
        ("users", "0006_alter_notepaluser_api_key"),
    ]

    operations = [
        migrations.AddField(
            model_name="notepaluser",
            name="session_id",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="sessions.session",
            ),
        ),
    ]
