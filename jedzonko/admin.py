from django.contrib import admin

# Register your models here.
from jedzonko.models import Recipe, Plan, Recipeplan, Dayname

admin.site.register(Recipe)
admin.site.register(Plan)
admin.site.register(Recipeplan)
admin.site.register(Dayname)