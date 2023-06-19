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
    reviews_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comments
        # read_only_fields = ('title_id',)


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
    category = CategoriesSerializer()
    genre = GenresSerializer(read_only=True, many=True)

    class Meta:
        fields = '__all__'
        model = Titles


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    title_id = serializers.PrimaryKeyRelatedField(read_only=True)

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
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User


class TitlesCreateUpdateSerializer(serializers.ModelSerializer):
    genre = serializers.ListSerializer(
        child=serializers.CharField()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all())

    class Meta:
        fields = '__all__'
        model = Titles

    def create(self, validated_data):
        genre_slugs = validated_data.pop('genre')
        title_name = validated_data.pop('name')
        title_year = validated_data.pop('year')
        category_slug = validated_data.pop('category')
        category = Categories.objects.get(slug=category_slug)
        title_description = validated_data.pop('description')

        title = Titles.objects.create(category=category,
                                      name=title_name,
                                      year=title_year,
                                      description=title_description)

        for genre_slug in genre_slugs:
            current_genre = Genres.objects.get(slug=genre_slug)
            genre_title = GenreTitle.objects.create(
                genre=current_genre, title=title)
            genre_title.save()
        return title
