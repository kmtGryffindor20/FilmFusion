# Generated by Django 4.2.5 on 2023-09-19 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0010_alter_movie_tmdb_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='cast',
        ),
        migrations.CreateModel(
            name='Cast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cast', models.TextField(blank=True, null=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='films.movie')),
            ],
        ),
    ]
