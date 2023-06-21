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
    """Сериализатор комментариев""" 
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    pub_date = serializers.DateField(format="%Y-%m-%dT%H:%M:%SZ")
    # reviews_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
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
    """Сериализатор произведений""" 
    category = CategoriesSerializer()
    genre = GenresSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category',)
        model = Titles

    def get_rating(self, obj):
        ratings = obj.reviews_title_id.all()
        scores = [rating.score for rating in ratings]
        if scores:
            average_score = round(sum(scores) / len(scores))
            return average_score
        return 0


class ReviewsSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов""" 
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    pub_date = serializers.DateField(format="%Y-%m-%dT%H:%M:%SZ")
    # title_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        model = Reviews


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей""" 

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User


class UserMeSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

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

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.year = validated_data.get('year', instance.year)
        instance.description = validated_data.get(
            'description', instance.description)

        category_slug = validated_data.pop('category')
        if category_slug:
            category = Categories.objects.get(slug=category_slug)
            instance.category = category

        genre_slugs = validated_data.pop('genre')
        if genre_slugs is not None:
            instance.genre.clear()
            for genre_slug in genre_slugs:
                current_genre = Genres.objects.get(slug=genre_slug)
                genre_title = GenreTitle.objects.create(
                    genre=current_genre, title=instance)
                genre_title.save()
        instance.save()
        return instance
