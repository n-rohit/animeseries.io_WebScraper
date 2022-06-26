from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User

class anime(models.Model):
    ANIMEUNKID = models.CharField(primary_key=True, max_length=255, null=False)
    ANIME_NAME = models.CharField(max_length=255)
    THUMB_IMAGE_LINK = models.TextField(max_length=500)
    DSCRIPTION = models.TextField(max_length=2000)
    CURRENT_STATUS = models.CharField(max_length=100)
    RELEASE_YEAR = models.IntegerField()
    GENRE = models.CharField(max_length=255)
    LATEST_EPISODE = models.CharField(max_length=255)
    LATEST_RELEASE_DATE = models.DateTimeField()

class episodes(models.Model):
    ANIMEUNKID = models.ForeignKey(anime, null=False, on_delete=CASCADE)
    EPISODEUNKID = models.CharField(primary_key=True, max_length=255, null=False)
    EPISODE_NUMBER = models.DecimalField(max_digits=5, decimal_places=2)
    EPISODE_TITLE = models.CharField(max_length=255)
    IS_VIDEO = models.TextField(max_length=500)
    VIDEO_DATA = models.TextField(max_length=2000)
    RELEASED_ON = models.IntegerField()
    EPISODE_VIDEO_BOX_LINK = models.TextField(max_length=500)
    # EPISODE_URL = models.TextField(max_length=500)