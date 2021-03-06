from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(
        blank=False,
        unique=True,
        max_length=254,
        verbose_name=_('Email адрес'),
        help_text=_('Email адрес пользователя.'),
    )

    password = models.CharField(
        max_length=150,
        verbose_name=_('Пароль'),
        help_text=_('В базе хранится хэш пароля.')
    )
    first_name = models.CharField(
        blank=False,
        max_length=150,
        verbose_name=_('Имя'),
        help_text=_('Имя пользователя.')
    )
    last_name = models.CharField(
        blank=False,
        max_length=150,
        verbose_name=_('Фамилия'),
        help_text=_('Фамилия пользователя.')
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name',)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name=_('Подписчик'),
        help_text=_('Пользователь, который подписывается'),
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name=_('Подписка'),
        help_text=_('Пользователь, на которого подписываются'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления записи'),
        help_text=_('Задается автоматически при обновлении записи.')
    )

    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'
        ordering = ('-updated_at',)
        constraints = [
            models.UniqueConstraint(fields=['user', 'following'],
                                    name='unique_subscription')
        ]

    def __str__(self):
        return f'{self.user.username} - {self.following.username}'
