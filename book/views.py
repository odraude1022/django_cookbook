from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from book.models import User
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
