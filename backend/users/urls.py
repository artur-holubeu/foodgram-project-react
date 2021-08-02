from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UsersView

app_name = "users"
router = DefaultRouter()
router.register(r'', UsersView)

urlpatterns = [
    # path('', include('djoser.urls')),
    # path('users/', UsersView.as_view()),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    path('users/', include(router.urls)),
]
