# Generated by Django 4.2.5 on 2023-09-18 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0003_rename_movie_id_review_movie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='director',
            name='director_name',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]