from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from book.models import User, Step, Ingredient, Recipe

class UserModelTest(TestCase):
  def test_username_uniqueness(self):
    user1 = User(email="something@example.com", username="hello123")
    user2 = User(email="somethingelse@example.com", username="goodbye123")
    user3 = User(email="somethingelse@example.com", username="hello123")
    user1.save()
    user2.save()
    self.assertRaises(IntegrityError, user3.save)

  def test_email_uniqueness(self):
    user1 = User(email="something@example.com", username="hello123")
    user2 = User(email="somethingelse@example.com", username="goodbye123")
    user3 = User(email="something@example.com", username="goodbye123")
    user1.save()
    user2.save()
    self.assertRaises(IntegrityError, user3.save)

class RecipeModelTest(TestCase):

  def test_name_not_null(self):
    user1 = User(email="something@example.com", username="hello123")
    user1.save()
    recipe1 = Recipe(user=user1)
    self.assertRaises(IntegrityError, recipe1.save)

  def test_user_not_null(self):
    recipe1 = Recipe(name="recipe1")
    self.assertRaises(IntegrityError, recipe1.save)


  def test_recipe_user_one_to_one(self):
    user1 = User(email="something@example.com", username="hello123")
    user2 = User(email="somethingelse@example.com", username="goodbye123")
    user1.save()
    user2.save()
    recipe1 = Recipe(name="recipe1", user=user2)
    recipe2 = Recipe(name="recipe2", user=user1)
    recipe3 = Recipe(name="recipe3", user=user1)
    recipe1.save()
    recipe2.save()
    self.assertEqual(recipe1.user, user2)
    self.assertEqual(user2.recipe, recipe1)
    self.assertRaises(IntegrityError, recipe3.save)

class StepModelTest(TestCase):
  def test_many_to_one_step_recipe(self):
    user1 = User(email="something@example.com", username="hello123")
    user2 = User(email="somethingelse@example.com", username="goodbye123")
    user1.save()
    user2.save()
    recipe1 = Recipe(name="recipe1", user=user1)
    recipe2 = Recipe(name="recipe2", user=user2)
    recipe1.save()
    recipe2.save()
    step1 = Step(step_text="do first thing", recipe=recipe1)
    step2 = Step(step_text="do second thing", recipe=recipe1)
    step3 = Step(step_text="do first thing for another thing", recipe=recipe2)
    step1.save()
    step2.save()
    step3.save()
    self.assertEqual(step1.recipe, recipe1)
    self.assertIn(step1, recipe1.step_set.all())
    self.assertIn(step2, recipe1.step_set.all())
    self.assertNotIn(step3, recipe1.step_set.all())


class IngredientModelTest(TestCase):
  def test_many_to_one_ingredient_recipe(self):
    user1 = User(email="something@example.com", username="hello123")
    user2 = User(email="somethingelse@example.com", username="goodbye123")
    user1.save()
    user2.save()
    recipe1 = Recipe(name="recipe1", user=user1)
    recipe2 = Recipe(name="recipe2", user=user2)
    recipe1.save()
    recipe2.save()
    ingredient1 = Ingredient(text="first ingredient", recipe=recipe1)
    ingredient2 = Ingredient(text="second ingredient", recipe=recipe1)
    ingredient3 = Ingredient(text="first ingredient of second recipe", recipe=recipe2)
    ingredient1.save()
    ingredient2.save()
    ingredient3.save()
    self.assertEqual(ingredient1.recipe, recipe1)
    self.assertIn(ingredient1, recipe1.ingredient_set.all())
    self.assertIn(ingredient2, recipe1.ingredient_set.all())
    self.assertNotIn(ingredient3, recipe1.ingredient_set.all())