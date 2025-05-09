# Generated by Django 5.0.2 on 2024-03-16 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_code', models.CharField(max_length=100)),
                ('game_creator', models.CharField(max_length=100)),
                ('game_opponent', models.CharField(blank=True, max_length=100, null=True)),
                ('is_over', models.BooleanField(default=False)),
            ],
        ),
    ]
