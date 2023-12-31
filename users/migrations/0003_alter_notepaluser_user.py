# Generated by Django 4.2.4 on 2023-08-19 21:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("users", "0002_remove_notepaluser_last_login_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notepaluser",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="notepaluser",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
