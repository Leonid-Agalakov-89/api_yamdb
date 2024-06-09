from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.fields import CharField, EmailField

from reviews.models import Category, Comment, Genre, Review, Title
from users.constants import (CONFIRMATION_CODE_LENGTH, EMAIL_LENGTH,
                             USERNAME_LENGTH)
from users.models import User
from users.validators import username_validator


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'category',
            'genre',
        )


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'category',
            'genre',
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'role', 'first_name', 'last_name', 'bio'
        )


class SignupSerializer(serializers.Serializer):
    username = CharField(max_length=USERNAME_LENGTH,
                         required=True,
                         validators=(UnicodeUsernameValidator(),
                                     username_validator))
    email = EmailField(max_length=EMAIL_LENGTH,
                       required=True)

    def create(self, validated_data):
        email = validated_data.get('email')
        username = validated_data.get('username')
        try:
            user, _ = User.objects.get_or_create(username=username,
                                                 email=email)
        except IntegrityError:
            raise serializers.ValidationError(
                'Пользователь с таким именем уже существует'
                if User.objects.filter(username=username).first()
                else 'Эта почта занята'
            )
        return user


class TokenSerializer(serializers.Serializer):
    username = CharField(
        max_length=USERNAME_LENGTH,
        required=True,
    )
    confirmation_code = CharField(
        max_length=CONFIRMATION_CODE_LENGTH,
        required=True
    )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        read_only_fields = (
            'title',
        )

    def validate(self, data):
        request = self.context['request']
        if (
            request.method == 'POST'
            and Review.objects.filter(
                author=request.user,
                title=get_object_or_404(
                    Title,
                    pk=self.context['view'].kwargs.get('title_id')
                )
            ).exists()
        ):
            raise serializers.ValidationError(
                'На это произведение уже есть отзыв.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
