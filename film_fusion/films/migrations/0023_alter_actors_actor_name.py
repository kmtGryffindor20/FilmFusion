# Generated by Django 4.2.5 on 2023-11-04 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0022_alter_actors_actor_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actors',
            name='actor_name',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
