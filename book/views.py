# from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from book.models import User, Recipe, Step, Ingredient
from book.serializers import UserSerializer, RecipeSerializer
import json

@csrf_exempt
def new_user(request):
  data = json.loads(request.body)
  username = data.get('username')
  email = data.get('email')
  first_name = data.get('first_name')
  last_name = data.get('last_name')

  new_user = User(username=username, email=email, first_name=first_name, last_name=last_name)
  try:
    new_user.save()

    serializer = UserSerializer(new_user)
    json_data = JSONRenderer().render(serializer.data)
    return HttpResponse(json_data)
  except Exception as e:
    return JsonResponse({"error": str(e)})

def get_all_users(request):
  data = User.objects.all()
  serializer = UserSerializer(data, many=True)
  json_data = JSONRenderer().render(serializer.data)

  return HttpResponse(json_data)

@csrf_exempt
def new_recipe(request):
  data = json.loads(request.body)
  user_id = data.get('user')
  name = data.get('name')

  new_recipe = Recipe(user_id=user_id, name=name)
  try:
    steps = list(data.get('steps'))
    ingredients = list(data.get('ingredients'))
    new_recipe.save()
    for step in steps:
      Step(recipe_id=new_recipe.pk, step_text=step).save()
      
    for ingredient in ingredients:
      Ingredient(recipe_id=new_recipe.pk, text=ingredient).save()

    serializer = RecipeSerializer(new_recipe)
    json_data = JSONRenderer().render(serializer.data)
    return HttpResponse(json_data)
  except Exception as e:
    return JsonResponse({"error": str(e)})
