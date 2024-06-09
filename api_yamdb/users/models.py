from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from users.constants import FIRST_LAST_NAME_LENGTH, USERNAME_LENGTH
from users.validators import username_validator


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    ROLES = (
        (USER, 'user'),
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator')
    )
    username = models.CharField('Имя пользователя',
                                max_length=USERNAME_LENGTH,
                                unique=True,
                                validators=(UnicodeUsernameValidator(),
                                            username_validator))
    email = models.EmailField('Электронная почта', unique=True)
    first_name = models.CharField('Имя',
                                  blank=True,
                                  max_length=FIRST_LAST_NAME_LENGTH)
    last_name = models.CharField('Фамилия',
                                 blank=True,
                                 max_length=FIRST_LAST_NAME_LENGTH)
    role = models.SlugField(choices=ROLES, default=USER)
    bio = models.TextField('Биография', blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return self.username
