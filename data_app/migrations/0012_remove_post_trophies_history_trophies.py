# Generated by Django 5.1.7 on 2025-04-13 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data_app", "0011_remove_history_trophies_post_trophies"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="trophies",
        ),
        migrations.AddField(
            model_name="history",
            name="trophies",
            field=models.JSONField(default=list),
        ),
    ]
