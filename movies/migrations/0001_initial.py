from django.db import migrations, models
import django.db.models.deletion
import cloudinary.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("category_name", models.CharField(max_length=255, unique=True)),
                (
                    "cover_url",
                    cloudinary.models.CloudinaryField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="category_covers",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "categories",
                "db_table": "movies_category",
            },
        ),
        migrations.CreateModel(
            name="CustomUser",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("username", models.CharField(max_length=255, unique=True)),
                ("first_name", models.CharField(blank=True, max_length=30)),
                ("last_name", models.CharField(blank=True, max_length=30)),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "movies_customuser",
            },
        ),
        migrations.CreateModel(
            name="Movie",
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
                ("title", models.CharField(max_length=255)),
                ("original_title", models.CharField(max_length=255)),
                ("original_language", models.CharField(default="en", max_length=10)),
                ("overview", models.TextField()),
                ("release_date", models.DateField()),
                ("popularity", models.FloatField(default=0)),
                ("vote_average", models.FloatField(default=0)),
                ("vote_count", models.IntegerField(default=0)),
                ("poster_path", models.URLField(blank=True, null=True)),
                ("backdrop_path", models.URLField(blank=True, null=True)),
                ("video", models.BooleanField(default=False)),
                ("adult", models.BooleanField(default=False)),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        db_column="category_id",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="movies",
                        to="movies.category",
                    ),
                ),
            ],
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
                        to="movies.customuser",
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "movie")},
            },
        ),
    ]
