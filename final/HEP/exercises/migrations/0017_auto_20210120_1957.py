# Generated by Django 3.1.5 on 2021-01-20 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0016_auto_20210119_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercisestats',
            name='exercise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to='exercises.exercise'),
        ),
    ]
