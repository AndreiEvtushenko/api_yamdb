from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from .mixins import GetListCreateObjectDelObject, AuthorSaveMixins

from reviews.models import Categories, Comments, Genres, Titles, Reviews
from .mixins import GetListCreateObjectDelObject, AuthorSaveMixins
from .serializers import (CategoriesSerializer, CommentsSerializer,
                          GenresSerializer, TitlesSerializer,
                          ReviewsSerializer, UserSerializer)

User = get_user_model()


class CategoriesViewSet(GetListCreateObjectDelObject):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination


class GenresViewSet(GetListCreateObjectDelObject):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('name', 'year', 'description', 'genre', 'category')
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination


class ReviewsViewSet(AuthorSaveMixins, viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        queryset = Reviews.objects.filter(title_id=title_id)
        return queryset


class CommentsViewSet(AuthorSaveMixins, viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        queryset = Comments.objects.filter(review_id=review_id)
        return queryset


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
