# Generated by Django 5.1.7 on 2025-04-08 22:41

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("data_app", "0006_remove_person_history_remove_post_person_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="History",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "analyzed_at",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("karma", models.IntegerField()),
                ("link_karma", models.IntegerField()),
                ("comment_karma", models.IntegerField()),
                ("is_mod", models.BooleanField()),
                ("is_employee", models.BooleanField()),
                ("is_gold", models.BooleanField()),
                ("verified", models.BooleanField()),
                ("has_verified_email", models.BooleanField()),
                ("bot_likelihood_percent", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Person",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=75, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("body", models.TextField()),
                ("score", models.IntegerField()),
                ("subreddit", models.CharField(max_length=100)),
                ("url", models.URLField()),
                ("created_date", models.DateField()),
                (
                    "history",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="data_app.history",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="history",
            name="person",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="histories",
                to="data_app.person",
            ),
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=300)),
                ("subreddit", models.CharField(max_length=100)),
                ("permalink", models.URLField()),
                ("url", models.URLField()),
                ("score", models.IntegerField()),
                ("upvotes_ratio", models.FloatField()),
                ("created_date", models.DateField()),
                ("num_comments", models.IntegerField()),
                ("over_18", models.BooleanField()),
                (
                    "history",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="posts",
                        to="data_app.history",
                    ),
                ),
            ],
        ),
    ]
