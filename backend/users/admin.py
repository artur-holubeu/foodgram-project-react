from django.contrib import admin

from .models import Subscription, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'first_name', 'last_name')
    search_fields = ('id', 'email', 'username')
    list_filter = ('email', 'username')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'following_name',)
    search_fields = ('id', 'user__username', 'user__email')

    def user_name(self, obj):
        return obj.auhtor.name

    def following_name(self, obj):
        return obj.following.name
