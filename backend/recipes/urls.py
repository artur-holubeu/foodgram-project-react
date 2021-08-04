from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TagView, RecipeView, IngredientView


app_name = "recipes"

router = DefaultRouter()
router.register(r'', RecipeView)

urlpatterns = [
    path('recipes/', include(router.urls)),
    path('tags/', TagView.as_view()),
    path('ingredients/', IngredientView.as_view()),
]