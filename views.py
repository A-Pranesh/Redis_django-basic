from django.http import HttpResponse
from django.shortcuts import render
from .models import User_Registration
from rest_framework.decorators import api_view
import jwt
import json
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
# Create your views here.

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
@api_view(['POST'])
def registration(request):
    data = json.loads(request.body.decode('utf-8'))
    user_object = User_Registration()
    user_object.Name = data['Name']
    user_object.Age = data['Age']
    user_object.Gender = data['Gender']
    user_object.save()
    return HttpResponse("done")

@api_view(['POST'])
def profile(request):
    data = json.loads(request.body.decode('utf-8'))
    result = cache.get(data['Name'])
    if result:
        print("Cache")
        return HttpResponse(result)
    else:
        user_object = User_Registration.objects.get(Name=data['Name'])
        cache.set(data['Name'], user_object, timeout=CACHE_TTL)
        print("DB")
        return HttpResponse(str(user_object))

@api_view(['POST'])
def delete_cache(request):
    data = json.loads(request.body.decode('utf-8'))
    cache.delete(data['Name'])
    return HttpResponse('deleted')