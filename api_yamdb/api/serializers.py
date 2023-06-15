from rest_framework import serializers

from reviews.models import Categories, Comments, Genres, Titles, Reviews
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

    class Meta:
        fields = ('name', 'slug',)
        model = Genres


class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        read_only=False,
        queryset=Categories.objects.all(),
        slug_field='name',
    )
    genre = serializers.SlugRelatedField(
        read_only=False,
        queryset=Genres.objects.all(),
        slug_field='name'
    )

    class Meta:
        fields = '__all__'
        model = Titles


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Reviews


class UserSerializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(
        read_only=False,
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = User
