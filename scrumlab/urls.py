from django.contrib import admin
from django.urls import path
from jedzonko.views import IndexView, MainView, DashboardView, \
    RecipesListView, PlanListView, AddRecipeView, AddPlanView, AddRecipeToPlanView, \
    RecipeDetailsView, RecipeModifyView, PlanDetailsView, PageDetailView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', IndexView.as_view()),
    path('', MainView.as_view(), name='main_view'),
    path('main/', DashboardView.as_view(), name='dashboard_view'),
    path('recipe/list/', RecipesListView.as_view(), name='recipe_list_view'),
    path('plan/list/', PlanListView.as_view(), name='plan_list'),
    path('recipe/add/', AddRecipeView.as_view(), name='add_recipe'),
    path('plan/add/', AddPlanView.as_view(), name='add_plan'),
    path('plan/add-recipe/', AddRecipeToPlanView.as_view(), name='add_recipe_to_plan'),
    path('recipe/<int:recipe_id>', RecipeDetailsView.as_view(), name='recipe_details' ),
    path('recipe/modify/<int:recipe_id>/', RecipeModifyView.as_view(), name='recipe_modify'),
    path('plan/<int:plan_id>/', PlanDetailsView.as_view(), name='plan_details'),
    path('page/<slug:slug>/', PageDetailView.as_view(), name='page_detail')
]
