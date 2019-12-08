from django.test import TestCase
from book.models import User, Recipe, Step, Ingredient
import json

new_user = {
  "username": "hello123",
  "email": "hello123@example.com",
  "first_name": "Hello",
  "last_name": "world"
}

new_user_only_username_and_email = {
  "username": "hello123",
  "email": "hello123@example.com"
}

class UserTest(TestCase):
  def test_can_create_new_user(self):
    response = self.client.post('/users/new', data=json.dumps(new_user), content_type="application/json")
    self.assertContains(response, "hello123")
    user = User.objects.first()
    self.assertEquals(user.username, "hello123")

  def test_can_create_user_with_only_username_and_email(self):
    response = self.client.post('/users/new', 
        data=json.dumps(new_user_only_username_and_email), 
        content_type="application/json"
    )
    self.assertContains(response, "hello123")
    user = User.objects.first()
    self.assertEquals(user.username, "hello123")

  def test_get_error_when_post_with_duplicate_data(self):
    self.client.post('/users/new', data=json.dumps(new_user), content_type="application/json")

    response = self.client.post('/users/new', data=json.dumps(new_user), content_type="application/json")
    self.assertContains(response, "error")

  def test_can_get_all_users(self):
    user1 = User(username="hello123", email="hello123@example.com")
    user1.save()
    user2 = User(username="goodbye123", email="goodbye123@example.com")
    user2.save()
    response = self.client.get('/users')
    self.assertContains(response, "hello123")
    self.assertContains(response, "goodbye123")

class RecipeTest(TestCase):
  def test_can_create_new_recipe(self):
    user1 = User(username="hello123", email="hello123@example.com")
    user1.save()
    new_recipe = {
      "name": "recipe 1",
      "user": User.objects.first().pk,
      "steps": [
        "Do first thing",
        "Do second thing",
        "Do third thing"
      ],
      "ingredients": [
        "First ingredient",
        "Second ingredient",
        "third ingredient"
      ]
    }

    response = self.client.post('/recipes/new', data=json.dumps(new_recipe), content_type="application/json")
    self.assertContains(response, 'recipe 1')

  def test_get_error_when_post_with_invalid_data(self):
    user1 = User(username="hello123", email="hello123@example.com")
    user1.save()
    new_recipe = {
      "name": "recipe 1",
      "steps": [
        "Do first thing",
        "Do second thing",
        "Do third thing"
      ],
      "ingredients": [
        "First ingredient",
        "Second ingredient",
        "third ingredient"
      ]
    }
    response = self.client.post('/recipes/new', data=json.dumps(new_recipe), content_type="application/json")
    self.assertContains(response, "error")

  def test_steps_get_linked_to_new_recipe(self):
    user1 = User(username="hello123", email="hello123@example.com")
    user2 = User(username='goodbye123', email="goodbye123@example.com")
    user1.save()
    user2.save()
    new_recipe_1 = {
      "name": "recipe 1",
      "user": user1.pk,
      "steps": [
        "Do first thing",
        "Do second thing",
        "Do third thing"
      ],
      "ingredients": [
        "First ingredient",
        "Second ingredient",
        "third ingredient"
      ]
    }
    new_recipe_2 = {
      "name": "recipe 2",
      "user": user2.pk,
      "steps": [
        "Do first thing again",
        "Do second thing again",
        "Do third thing again"
      ],
      "ingredients": [
        "First ingredient again",
        "Second ingredient again",
        "third ingredient again"
      ]
    }
    response1 = json.loads(self.client.post('/recipes/new', data=json.dumps(new_recipe_1), content_type="application/json").content)
    response2 = json.loads(self.client.post('/recipes/new', data=json.dumps(new_recipe_2), content_type="application/json").content)
    recipe1 = Recipe.objects.get(pk=response1[0]['pk'])
    recipe2 = Recipe.objects.get(pk=response2[0]['pk'])
    steps1 = recipe1.step_set.all()
    steps2 = recipe2.step_set.all()
    step3 = Step.objects.get(step_text="Do third thing")
    self.assertIn(step3, steps1)
    self.assertNotIn(step3, steps2)
  
  def test_ingredients_get_linked_to_new_recipe(self):
    user1 = User(username="hello123", email="hello123@example.com")
    user2 = User(username='goodbye123', email="goodbye123@example.com")
    user1.save()
    user2.save()
    new_recipe_1 = {
      "name": "recipe 1",
      "user": user1.pk,
      "steps": [
        "Do first thing",
        "Do second thing",
        "Do third thing"
      ],
      "ingredients": [
        "First ingredient",
        "Second ingredient",
        "third ingredient"
      ]
    }
    new_recipe_2 = {
      "name": "recipe 2",
      "user": user2.pk,
      "steps": [
        "Do first thing again",
        "Do second thing again",
        "Do third thing again"
      ],
      "ingredients": [
        "First ingredient again",
        "Second ingredient again",
        "third ingredient again"
      ]
    }
    response1 = json.loads(self.client.post('/recipes/new', data=json.dumps(new_recipe_1), content_type="application/json").content)
    response2 = json.loads(self.client.post('/recipes/new', data=json.dumps(new_recipe_2), content_type="application/json").content)
    recipe1 = Recipe.objects.get(pk=response1[0]['pk'])
    recipe2 = Recipe.objects.get(pk=response2[0]['pk'])





    ingredients1 = recipe1.ingredient_set.all()
    ingredients2 = recipe2.ingredient_set.all()
    ingredient3 = Ingredient.objects.get(text="third ingredient")
    self.assertIn(ingredient3, ingredients1)
    self.assertNotIn(ingredient3, ingredients2)



