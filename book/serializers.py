from rest_framework import serializers
from book.models import User, Recipe, Step, Ingredient

class RecipeSerializer(serializers.ModelSerializer):
  ingredient_set = serializers.StringRelatedField(many=True)
  step_set = serializers.StringRelatedField(many=True)
  class Meta:
    model = Recipe
    fields = ['pk', 'name', 'user_id', 'step_set', 'ingredient_set']