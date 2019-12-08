# from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
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

def get_user(request, user_id):
  try:
    data = User.objects.get(pk=user_id)
    serializer = UserSerializer(data)
    json_data = JSONRenderer().render(serializer.data)

    return HttpResponse(json_data)
  except ObjectDoesNotExist as e:
    return JsonResponse({"error": "No user exists with this id"})

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

@csrf_exempt
def single_recipe(request, recipe_id):
  if(request.method == 'PATCH'):
    return update_recipe(request, recipe_id)
  elif(request.method == 'DELETE'):
    return delete_recipe(request, recipe_id)

def update_recipe(request, recipe_id):
  recipe = Recipe.objects.get(pk=recipe_id)
  data = json.loads(request.body)
  name = data.get('name')
  steps = []
  ingredients = []
  try:
    steps = list(data.get('steps'))
  except Exception as e:
    pass
  try:
    ingredients = list(data.get('ingredients'))
  except Exception as e:
    pass
  if steps:
    recipe.step_set.all().delete()
    for step in steps:
      Step(recipe_id=recipe.pk, step_text=step).save()

  if ingredients:
    recipe.ingredient_set.all().delete()
    for ingredient in ingredients:
      Ingredient(recipe_id=recipe.pk, text=ingredient).save()

  if name:
    recipe.name = name

  recipe.save()
  serializer = RecipeSerializer(recipe)
  json_data = JSONRenderer().render(serializer.data)
  return HttpResponse(json_data)

def delete_recipe(request, recipe_id):
  recipe = Recipe.objects.get(pk=recipe_id)
  serializer = RecipeSerializer(recipe)
  json_data = JSONRenderer().render(serializer.data)
  recipe.delete()
  return HttpResponse(json_data)






