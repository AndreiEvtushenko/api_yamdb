from django.contrib.auth import get_user_model

lViewsfrom rest_framework import status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from .mixins import GetListCreateObjectDelObject, AuthorSaveMixins


from reviews.models import Categories, Comments, Genres, Titles, Reviews
from .mixins import (AuthorSaveMixins, GetListCreateObject,
                     GetListCreateRetrieveObject)
from .serializers import (CategoriesSerializer, CommentsSerializer,
                          GenresSerializer, TitlesSerializer,
                          ReviewsSerializer, UserSerializer)

User = get_user_model()


class CategoriesViewSet(GetListCreateObject):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination


class CategoriesDel(APIView):

    def delete(self, request, *args, **kwargs):
        if request.method == 'DELETE':
            categories = self.kwargs.get('slug')
            try:
                categories = Categories.objects.get(slug=categories)
                categories.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Categories.DoesNotExist:
                return Response(
                    data="Категория не найден", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenresViewSet(GetListCreateObject):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination


class GenresDel(APIView):

    def delete(self, request, *args, **kwargs):
        if request.method == 'DELETE':
            slug_genres = self.kwargs.get('slug')
            try:
                genres = Genres.objects.get(slug=slug_genres)
                genres.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Genres.DoesNotExist:
                return Response(
                    data="Жанр не найден", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


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


class UserViewSet(GetListCreateRetrieveObject):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination


class UsersDel(APIView):

    def delete(self, request, *args, **kwargs):
        if request.method == 'DELETE':
            username = self.kwargs.get('username')
            try:
                user = User.objects.get(username=username)
                user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except User.DoesNotExist:
                return Response(
                    data="Пользователь не найден",
                    status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
