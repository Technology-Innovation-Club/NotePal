# Generated by Django 4.2.4 on 2023-08-14 19:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="history",
            name="embedding_context",
            field=models.JSONField(blank=True, null=True),
        ),
    ]
