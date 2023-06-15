from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .mixins import GetListCreateObjectDelObject, AuthorSaveMixins

from reviews.models import Categories, Comments, Genres, Titles, Reviews
from .serializers import (CategoriesSerializer, CommentsSerializer,
                          GenresSerializer, TitlesSerializer,
                          ReviewsSerializer, UsersSerializers)

User = get_user_model()


class CategoriesViewSet(GetListCreateObjectDelObject):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(GetListCreateObjectDelObject):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer


class ReviewsViewSet(AuthorSaveMixins, viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        queryset = Reviews.objects.filter(title_id=title_id)
        return queryset


class CommentsViewSet(AuthorSaveMixins, viewsets.ModelViewSet):
    serializer_class = CommentsSerializer

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        queryset = Comments.objects.filter(review_id=review_id)
        return queryset


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializers
