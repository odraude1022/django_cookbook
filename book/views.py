from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from book.models import User, Recipe, Step, Ingredient
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
    serialized_data = serializers.serialize('json', [ new_user])  
    return HttpResponse(serialized_data)
  except Exception as e:
    return JsonResponse({"error": str(e)})

def get_all_users(request):
  data = User.objects.all()
  serialized_data = serializers.serialize('json', data)
  return HttpResponse(serialized_data)

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
    serialized_data = serializers.serialize('json', [new_recipe])
    return HttpResponse(serialized_data)
  except Exception as e:
    return JsonResponse({"error": str(e)})
