from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SubscribeView, SubscriptionsListView, UsersView

app_name = "users"
router = DefaultRouter()
router.register(r'', UsersView)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    path('users/subscriptions/', SubscriptionsListView.as_view({
        'get': 'list'
    })),
    path('users/<int:author_id>/subscribe/', SubscribeView.as_view({
        'get': 'create',
        'delete': 'destroy'
    })),
    path('users/', include(router.urls)),
]
