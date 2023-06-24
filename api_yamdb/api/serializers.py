from rest_framework import serializers
from django.utils import timezone

from reviews.models import Categories, Comments, Genres, Title, Review
from .constants import USERNAME_ERROR_MESSAGE, USERNAME_REQUIRED_ERROR
from .utils.get_rating import get_rating
from users.models import User

PUB_DATE = serializers.DateField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор категорий"""

    class Meta:
        fields = ('name', 'slug',)
        model = Categories


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев"""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    pub_date = PUB_DATE

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comments


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор жанров"""

    class Meta:
        fields = ('name', 'slug',)
        model = Genres

    def validate_slug(self, value):
        if Genres.objects.filter(slug=value).exists():
            raise serializers.ValidationError(
                f'Вы указали: {value}.'
                'Такой slug уже занят'
            )
        return value


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализатор проиведений для GET запросов"""
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category',)
        model = Title

    def get_rating(self, obj):
        return get_rating(self, obj)


class ReviewsSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов"""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    pub_date = PUB_DATE

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        model = Review


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей"""

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User


class UserMeSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя для запроса /users/me/"""
    role = serializers.CharField(read_only=True)

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User


class TitlesCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор проиведений для небезопасных запросов"""
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genres.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title

    def validate(self, attrs):
        name = attrs.get('name')
        year = attrs.get('year')

        if not name:
            raise serializers.ValidationError(
                'Поле не может быть пустым.'
                f'Вы указали название: {name}.'
                )

        if len(name) > 256:
            raise serializers.ValidationError('Название не более 256 символов')

        current_year = timezone.now().year

        if year and year > current_year:
            raise serializers.ValidationError(
                f'Год выпуска произведения не может быть больше текущего.'
                f'Вы указали: "{year}", текущий год: "{current_year}".'
            )

        return attrs

    def get_rating(self, obj):
        return get_rating(self, obj)


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True,
        error_messages={
            'invalid': USERNAME_ERROR_MESSAGE,
            'required': USERNAME_REQUIRED_ERROR,
        }
    )
    email = serializers.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if not value:
            raise serializers.ValidationError('Username не может быть пустым.')

        if value == 'me':
            raise serializers.ValidationError('Нельзя использовать me')
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
