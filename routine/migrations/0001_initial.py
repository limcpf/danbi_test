# Generated by Django 4.1.6 on 2023-02-05 20:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Routine",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("routine_id", models.BigAutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255)),
                (
                    "category",
                    models.CharField(
                        choices=[("M", "MIRACLE"), ("H", "HOMEWORK")], max_length=2
                    ),
                ),
                ("goal", models.TextField()),
                ("is_alarm", models.BooleanField(default=False)),
                ("is_deleted", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="RoutineResult",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "routine_result_id",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                (
                    "result",
                    models.CharField(
                        choices=[("N", "NOT"), ("T", "TRY"), ("D", "DONE")],
                        default="N",
                        max_length=2,
                    ),
                ),
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "routine",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="routine.routine",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="RoutineDay",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "day",
                    models.IntegerField(
                        choices=[
                            (0, "MON"),
                            (1, "TUE"),
                            (2, "WED"),
                            (3, "THU"),
                            (4, "FRI"),
                            (5, "SAT"),
                            (6, "SUN"),
                        ]
                    ),
                ),
                (
                    "routine",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="routine.routine",
                    ),
                ),
            ],
        ),
    ]
