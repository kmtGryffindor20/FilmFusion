# Generated by Django 4.2.5 on 2023-09-19 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0007_movie_tmdb_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='movie_api_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='release_date',
            field=models.DateField(null=True),
        ),
    ]
