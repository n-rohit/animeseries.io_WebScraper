from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from AnimeApp.models import anime,episodes
from AnimeApp.serializers import animeSerializers,episodesSerializers
from django.core.files.storage import default_storage


@csrf_exempt
def get_all_anime(request):
    if request.method == 'GET':
        Anime = anime.objects.all()
        Anime_Serializers = animeSerializers(Anime,many=True)
        return JsonResponse(Anime_Serializers.data, safe=False)

@csrf_exempt
def get_all_anime_by_alphabet(request,letter='A'):
    if request.method == 'GET':
        Anime = anime.objects.get(ANIMEUNKID=letter)
        Anime_Serializers = animeSerializers(Anime,many=True)
        return JsonResponse(Anime_Serializers.data, safe=False)

@csrf_exempt
def get_all_anime_by_animeunkid(request,id=0):
    if request.method == 'GET':
        Anime = anime.objects.get(ANIMEUNKID=id)
        Anime_Serializers = animeSerializers(Anime,many=True)
        return JsonResponse(Anime_Serializers.data, safe=False)

@csrf_exempt
def search_anime(request):
    if request.method == 'GET':
        Anime = anime.objects.get()
        Anime_Serializers = animeSerializers(Anime,many=True)
        return JsonResponse(Anime_Serializers.data, safe=False)

@csrf_exempt
def get_all_episodes(request):
    if request.method == 'GET':
        Episodes = episodes.objects.all()
        Episodes_Serializers = episodesSerializers(Episodes,many=True)
        return JsonResponse(Episodes_Serializers.data, safe=False)

@csrf_exempt
def get_all_anime_by_episodeunkid(request,id=0):
    if request.method == 'GET':
        Anime = anime.objects.get(EPISODEUNKID=id)
        Anime_Serializers = animeSerializers(Anime,many=True)
        return JsonResponse(Anime_Serializers.data, safe=False)

@csrf_exempt
def create_anime(request,id=0):
    if request.method == 'POST':
        Anime_Data = JSONParser().parse(request)
        Anime_Serializers = animeSerializers(data=Anime_Data)
        if Anime_Serializers.is_valid():
            Anime_Serializers.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)

@csrf_exempt
def create_episode(request,id=0):
    if request.method == 'POST':
        Episode_Data = JSONParser().parse(request)
        Episodes_Serializers = episodesSerializers(data=Episode_Data)
        if Episodes_Serializers.is_valid():
            Episodes_Serializers.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)

# @csrf_exempt
# def delete_anime(request,id=0):
#     if request.method == 'DELETE':
#         Anime = anime.objects.get(ANIMEUNKID=id)
#         Anime.delete()
#         return JsonResponse("Deleted Successfully", safe=False)