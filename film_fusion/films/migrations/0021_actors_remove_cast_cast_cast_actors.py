# Generated by Django 4.2.5 on 2023-11-04 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0020_movie_popularity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actor_api_id', models.IntegerField(null=True, unique=True)),
                ('actor_name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='cast',
            name='cast',
        ),
        migrations.AddField(
            model_name='cast',
            name='actors',
            field=models.ManyToManyField(to='films.actors'),
        ),
    ]
