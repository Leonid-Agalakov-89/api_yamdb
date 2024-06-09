from datetime import datetime as dt

from rest_framework import serializers


def validate_year(year):
    if year > dt.now().year:
        raise serializers.ValidationError(
            'Год выпуска не может быть больше текущего'
        )
