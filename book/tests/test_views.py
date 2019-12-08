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

  def test_get_error_when_post_with_invalid_data(self):
    self.client.post('/users/new', data=json.dumps(new_user), content_type="application/json")

    response = self.client.post('/users/new', data=json.dumps(new_user), content_type="application/json")
    self.assertContains(response, "error")