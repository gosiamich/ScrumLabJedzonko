from datetime import datetime
from jedzonko.models import Recipe, Plan, Recipeplan, Dayname, Page
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from django.core.exceptions import ObjectDoesNotExist


class IndexView(View):
    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class MainView(View):
    def get(self, request):
        ctx = {
            'carousel_items': Recipe.objects.order_by('?').all()[:3]
        }
        return render(request, 'index.html', ctx)


class DashboardView(View):
    def get(self, request):
        last_added_plan = {
            'object': None,
            'recipes': []
        }

        try:
            plan = Plan.objects.order_by('-created')[0]
            last_added_plan['object'] = plan
            for recipeplan in plan.recipeplan_set.order_by('day_name__order', 'order').all():
                last_added_plan['recipes'].append({
                    'dayname': recipeplan.day_name.name,
                    'meal_name': recipeplan.meal_name,
                    'recipe_name': recipeplan.recipe.name,
                    'recipe_id': recipeplan.recipe.id,
                })
        except ObjectDoesNotExist:
            pass

        ctx = {
            'recipe_count': Recipe.objects.count(),
            'plans_count': Plan.objects.count(),
            'last_added_plan': last_added_plan,
        }
        return render(request, 'dashboard.html', ctx)

class RecipesListView(ListView):
    model = Recipe
    template_name = 'app-recipes.html'
    ordering = ['-votes', '-created']


class PlanListView(ListView):
    model = Plan
    template_name = 'app-schedules.html'

class PageDetailView(View):
    def get(self, request, slug):
        if Page.objects.get(slug=slug):
            return render(request, 'page.html', {'page': Page.objects.get(slug=slug)})
        else:
            return redirect(f'/#{slug}')


class AddRecipeView(View):
    def get(self, request):
        return render(request, 'app-add-recipe.html')
    def post(self, request):
        recipe_name = request.POST.get('recipe_name')
        description = request.POST.get('description')
        time = request.POST.get('time')
        ingredients = request.POST.get('ingredients')

        if recipe_name != "" and description != "" and time != "" and ingredients !="":
            Recipe.objects.create(
                name = recipe_name,
                ingredients = ingredients,
                description = description,
                preparation_time = time
            )
            return redirect('recipe_list_view')
        return render(request, 'app-add-recipe.html', {'error': 'Wypełnij poprawnie wszystkie pola'} )


class AddPlanView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'app-add-schedules.html')

    def post(self, request):
        plan_name = request.POST.get('plan_name')
        plan_description = request.POST.get('plan_description')

        if plan_name == "" or plan_description == "":
            message = "Pola muszą być uzupełnione"
            return render(request, 'app-add-schedules.html', {'message': message})

        plan = Plan.objects.create(
            name = plan_name,
            description = plan_description
        )
        id = plan.id
        return redirect(reverse('plan_details', kwargs={'plan_id': id}))


class AddRecipeToPlanView(View):
    def get(self, request):
        Plans = Plan.objects.all()
        DayName = Dayname.objects.all()
        Recipes = Recipe.objects.all()
        return render(request, 'app-schedules-meal-recipe.html', {'Plans':Plans, 'Recipes': Recipes,'DayName': DayName})
    def post(self, request):
        choosePlanName = request.POST.get('choosePlanName')
        mealName = request.POST.get('mealName')
        mealNumber= request.POST.get('recipeNumber')
        recipeName = request.POST.get('recipeName')
        dayNameName= request.POST.get('dayName')

        plan = Plan.objects.get(name=choosePlanName)
        recipe = Recipe.objects.get(name=recipeName)
        dayname = Dayname.objects.get(name=dayNameName)
        id = plan.id
        Recipeplan.objects.create(meal_name=mealName,order=mealNumber, day_name=dayname, plan=plan, recipe=recipe)
        return redirect(reverse('plan_details', kwargs={"plan_id": id}))


class RecipeDetailsView(View):
    def get(self, request, recipe_id):
        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            raise Http404('Brak przepisu o podanym id')
        return render(request, 'app-recipe-details.html', {'recipe': recipe})

    def post(self, request, recipe_id):
        recipe_id = request.POST.get('recipe_id')
        action_type = request.POST.get('action_type')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if action_type == 'like':
            recipe.votes += 1
        elif action_type == 'dislike':
            recipe.votes -= 1
        else:
            raise Http404('Unsupported action type')
        recipe.save()
        return redirect('recipe_details', recipe_id=recipe_id)


class RecipeModifyView(View):
    def get(self, request, recipe_id):
        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            raise Http404('Brak przepisu o podanym id')
        return render(request, 'app-edit-recipe.html', {'recipe':recipe})

    def post(self, request, recipe_id):
        name = request.POST.get('name')
        description = request.POST.get('description')
        preparation_time = request.POST.get('preparation_time')
        ingredients = request.POST.get('ingredients')

        if name != "" and description != "" and preparation_time != "" and ingredients != "":
            Recipe.objects.create(
                name = name,
                ingredients = ingredients,
                description = description,
                preparation_time = preparation_time
            )
        else:
            recipe = Recipe.objects.get(id=recipe_id)
            error = "Pola muszą być uzupełnione"
            return render(request, 'app-edit-recipe.html', {'recipe': recipe, 'error': error})
        return redirect('recipe_list_view')


class PlanDetailsView(View):
    def get(self, request, plan_id):
        plan = Plan.objects.get(id=plan_id)
        recipes_plans = plan.recipeplan_set.all().order_by('order')
        day_and_meals = []
        for i in range(1, 8):
            recipes_for_day = recipes_plans.filter(day_name__order=i)
            if len(recipes_for_day) > 0:
                day_and_meals.append((recipes_for_day[0].day_name, recipes_for_day))
        return render(request, 'app-details-schedules.html', {'plan': plan,'day_and_meals': day_and_meals})
