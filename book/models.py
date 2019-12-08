from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

class User(models.Model):
  username = models.CharField(max_length=20, unique=True)
  email = models.EmailField(unique=True)
  first_name = models.CharField(max_length=35, null=True, blank=True)
  last_name = models.CharField(max_length=35, null=True, blank=True)
  REQUIRED_FIELDS = []
  USERNAME_FIELD = 'username'
  is_anonymous = False
  is_authenticated = True

class Recipe(models.Model):
  name = models.CharField(max_length=30, default=None)
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)

class Step(models.Model):
  step_text = models.TextField(default=None)
  recipe = models.ForeignKey(Recipe, default=None, on_delete=models.CASCADE)

class Ingredient(models.Model):
  text = models.CharField(max_length=30, default=None)
  recipe = models.ForeignKey(Recipe, default=None, on_delete=models.CASCADE)

