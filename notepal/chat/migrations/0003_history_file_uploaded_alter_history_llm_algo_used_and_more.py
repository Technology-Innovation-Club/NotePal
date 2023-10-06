# Generated by Django 4.1.7 on 2023-10-05 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("note", "0001_initial"),
        ("chat", "0002_alter_noteembedding_file_embedding"),
    ]

    operations = [
        migrations.AddField(
            model_name="history",
            name="file_uploaded",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="note.notefileembedding",
            ),
        ),
        migrations.AlterField(
            model_name="history",
            name="llm_algo_used",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="history",
            name="llm_response",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="history",
            name="response_to_user",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="history",
            name="user_question",
            field=models.TextField(blank=True, null=True),
        ),
    ]
