# Generated by Django 4.1.2 on 2023-08-01 13:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("users", "0007_uploadedimage_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="UploadVideo",
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
                ("video", models.FileField(max_length=254, upload_to="profile_images")),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                ("others", models.TextField(blank=True, default="Others", null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
