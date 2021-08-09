from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'recipes'

router = DefaultRouter()
router.register('tags', TagView)
router.register('ingredients', IngredientView)
router.register('recipes', RecipeView)

urlpatterns = [
    # path('favorites/', FavoriteListView.as_view({'get': 'list'})),
    # path('cart/', ShoppingCartView.as_view({'get': 'list'})),
    path('recipes/<int:recipe_id>/favorite/', FavoriteView.as_view(
        {
            'get': 'create',
            'delete': 'destroy'
        }
    )),
    path('recipes/<int:recipe_id>/shopping_cart/',
         ShoppingCartView.as_view(
             {
                 'get': 'create',
                 'delete': 'destroy'
             }
         )),
    path('recipes/download_shopping_cart/', download_shopping_cart,
         name='download_pdf'),
    path('', include(router.urls)),
]
