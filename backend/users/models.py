from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Реализация модели User с необходимыми дополнительными полями."""

    email = models.EmailField(
        blank=False,
        unique=True,
        max_length=254,
        verbose_name=_('Email адрес'),
        help_text=_('Email пользователя')
    )

    password = models.CharField(
        max_length=150,
        verbose_name=_('Пароль'),
        help_text=_('В базе хранится хэш пароля, поэтому не стоит '
                    'переживать за утечки данных с нашего сервиса)')
    )
    first_name = models.CharField(
        blank=False,
        max_length=150,
        verbose_name=_('Имя'),
        help_text=_('Имя пользователя')
    )
    last_name = models.CharField(
        blank=False,
        max_length=150,
        verbose_name=_('Фамилия'),
        help_text=_('Фамилия пользователя')
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['id']


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Подписчик",
        related_name="follower",
        help_text="Пользователь, который подписывается",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Подписка",
        related_name="following",
        help_text="Пользователь, на которого подписываются",
    )

    def __str__(self):
        return self.user

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "author"],
                                    name="unique_follow")
        ]
