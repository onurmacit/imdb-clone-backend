# Generated by Django 4.2.19 on 2025-03-17 18:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0005_rename_name_category_category_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="movie",
            old_name="description",
            new_name="overview",
        ),
        migrations.RemoveField(
            model_name="movie",
            name="rating",
        ),
        migrations.AddField(
            model_name="movie",
            name="adult",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="movie",
            name="backdrop_path",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="movie",
            name="categories",
            field=models.ManyToManyField(related_name="movies", to="movies.category"),
        ),
        migrations.AddField(
            model_name="movie",
            name="original_language",
            field=models.CharField(default="en", max_length=10),
        ),
        migrations.AddField(
            model_name="movie",
            name="original_title",
            field=models.CharField(default="Unknown", max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="movie",
            name="popularity",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="movie",
            name="poster_path",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="movie",
            name="video",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="movie",
            name="vote_average",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="movie",
            name="vote_count",
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name="Rating",
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
                ("score", models.IntegerField(default=1)),
                (
                    "movie",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ratings",
                        to="movies.movie",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "movie")},
            },
        ),
    ]
