# Generated by Django 4.2.5 on 2023-11-05 13:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('films', '0025_alter_video_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show', models.IntegerField(choices=[('0', '9:00 AM'), ('1', '12:00 PM'), ('2', '3:00 PM'), ('3', '6:00 PM'), ('4', '9:00 PM')])),
                ('seat', models.CharField(max_length=10)),
                ('ticket_id', models.CharField(max_length=100)),
                ('booked_at', models.DateTimeField(auto_now_add=True)),
                ('price', models.IntegerField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='films.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]