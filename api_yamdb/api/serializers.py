# from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from reviews.models import (
    Categories, Comments, Genres, GenreTitle, Titles, Reviews
)
from users.models import User


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        model = Categories


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comments
        read_only_fields = ('title_id',)


class GenresSerializer(serializers.ModelSerializer):
    # Если ставим валидацию, то при добавлении Title, там тоже идет проверка
    # на уникальность и объект не добавляется

    # name = serializers.CharField(
    #     required=True,
    #     validators=[
    #         UniqueValidator(
    #             queryset=Genres.objects.all(),
    #             message="Жанр с таким именем уже существует."
    #         )
    #     ]
    # )

    class Meta:
        fields = ('name', 'slug',)
        model = Genres


class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        read_only=False,
        queryset=Categories.objects.all(),
        slug_field='name',
    )
    genre = GenresSerializer(many=True,)

    class Meta:
        fields = '__all__'
        model = Titles

    # проблема в том, что в теории данные поля не были уникальными
    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Titles.objects.create(**validated_data)
        for genre in genres:
            current_genre, status = Genres.objects.get_or_create(**genre)
            GenreTitle.objects.create(genre=current_genre, title=title)
        return title


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Reviews


class UserSerializer(serializers.ModelSerializer):
    # Эта часть кода не работает, пришлось закомментить
    # username = serializers.SlugRelatedField(
    #     read_only=False,
    #     queryset=User.objects.all(),
    #     slug_field='username'
    # )

    class Meta:
        fields = '__all__'
        model = User
