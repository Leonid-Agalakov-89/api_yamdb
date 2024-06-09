from django.core.exceptions import ValidationError


def username_validator(value):
    if value == 'me':
        raise ValidationError(
            'Для имени пользователя нельзя использовать «me»'
        )
    return value
