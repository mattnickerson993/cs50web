# Generated by Django 3.1.5 on 2021-01-19 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0008_auto_20210119_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercisestats',
            name='notes',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
    ]