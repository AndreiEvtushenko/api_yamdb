from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Categories, Comments, Genres, Titles, Reviews


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name',)
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
        fields = ('name',)
        model = Genres


class TitlesSerializer(serializers.ModelSerializer):

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
