# Generated by Django 3.2.5 on 2021-08-14 04:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='anime',
            fields=[
                ('ANIMEUNKID', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('ANIME_NAME', models.CharField(max_length=255)),
                ('THUMB_IMAGE_LINK', models.TextField(max_length=500)),
                ('DSCRIPTION', models.TextField(max_length=2000)),
                ('CURRENT_STATUS', models.CharField(max_length=100)),
                ('RELEASE_YEAR', models.IntegerField()),
                ('GENRE', models.CharField(max_length=255)),
                ('LATEST_EPISODE', models.CharField(max_length=255)),
                ('LATEST_RELEASE_DATE', models.DateTimeField()),
                ('VIDEO_BOX_LINK', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='epsiodes',
            fields=[
                ('EPSIODEUNKID', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('EPISODE_NUMBER', models.DecimalField(decimal_places=2, max_digits=5)),
                ('EPISODE_TITLE', models.CharField(max_length=255)),
                ('IS_VIDEO', models.TextField(max_length=500)),
                ('VIDEO_DATA', models.TextField(max_length=2000)),
                ('RELEASED_ON', models.IntegerField()),
                ('EPISODE_URL', models.TextField(max_length=500)),
                ('ANIMEUNKID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AnimeApp.anime')),
            ],
        ),
    ]