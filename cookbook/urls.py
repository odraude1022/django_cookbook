from django.contrib import admin
from django.conf.urls import url
from django.urls import path
from book import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^users/new$', views.new_user, name="new_user"),
    url(r'^users$', views.get_all_users, name="get_all_users"),
    url(r'^recipes/new$', views.new_recipe, name="new_recipe")
]
