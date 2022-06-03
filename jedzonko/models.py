from django.db import models

# Create your models here.


class Recipe(models.Model):
    name = models.CharField(max_length=254)
    ingredients = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    preparation_time = models.PositiveSmallIntegerField()
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Plan(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    recipes = models.ManyToManyField(Recipe, through='Recipeplan')

class Dayname(models.Model):
    name = models.CharField(max_length=64)
    order = models.PositiveSmallIntegerField(unique=True)

class Recipeplan(models.Model):
    meal_name = models.CharField(max_length=64)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField()
    day_name = models.ForeignKey(Dayname, on_delete=models.CASCADE)

class Page(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.title


