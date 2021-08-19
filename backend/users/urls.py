from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SubscriptionsListView, UsersView

app_name = "users"
router = DefaultRouter()
router.register(r'', UsersView)

urlpatterns = [
    path(
        'users/subscriptions/',
        SubscriptionsListView.as_view({'get': 'list'}),
        name='subscriptions'
    ),
    path(
        'users/<int:following_id>/subscribe/',
        SubscriptionsListView.as_view({'get': 'create', 'delete': 'destroy'}),
        name='subscribe'
    ),
    path('users/', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
]
