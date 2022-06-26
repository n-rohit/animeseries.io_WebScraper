from django.db.models import fields
from rest_framework import serializers
from AnimeApp.models import anime,episodes

class animeSerializers(serializers.ModelSerializer):
    class Meta:
        model = anime
        fields = ('ANIMEUNKID','ANIME_NAME','THUMB_IMAGE_LINK','DSCRIPTION','CURRENT_STATUS','RELEASE_YEAR','GENRE','LATEST_EPISODE','LATEST_RELEASE_DATE')

class episodesSerializers(serializers.ModelSerializer):
    class Meta:
        model = episodes
        fields = ('ANIMEUNKID','EPISODEUNKID','EPISODE_NUMBER','EPISODE_TITLE','IS_VIDEO','VIDEO_DATA','RELEASED_ON','EPISODE_VIDEO_BOX_LINK',)