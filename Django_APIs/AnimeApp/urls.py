from django.conf.urls import url
from AnimeApp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url('animes', views.get_all_anime),
    url('anime/alphabet',views.get_all_anime_by_alphabet),
    url('anime/(ANIME000+([0-9]+))',views.get_all_anime_by_animeunkid),
    # url('animes', views.search_anime),
    url('episodes', views.get_all_episodes),
    url('anime/(EPISODE)', views.get_all_anime_by_episodeunkid),
    url('postanime',views.create_anime),
    url('postepisode',views.create_episode),
]