from rest_framework import viewsets
from .mixins import GetListCreateObjectDelObject, AuthorSaveMixins

from .models import Categories, Comments, Genres, Title, Reviews
from .serializers import (CategoriesSerializers, CommentsSerializers,
                          GenresSerializers, TitleSerializers,
                          ReviewsSerializers)


class Categories(AuthorSaveMixins, GetListCreateObjectDelObject):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializers


class GenresViewSet(AuthorSaveMixins, GetListCreateObjectDelObject):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializers


class TitleViewSet(AuthorSaveMixins, viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializers


class ReviewsViewSet(AuthorSaveMixins, viewsets.ModelViewSet):
    serializer_class = ReviewsSerializers

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        queryset = Reviews.objects.filter(title_id=title_id)
        return queryset


class CommentsViewSet(AuthorSaveMixins, viewsets.ModelViewSet):
    serializer_class = CommentsSerializers

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        queryset = Comments.objects.filter(review_id=review_id)
        return queryset


class UsersViewSet(viewsets.ModelViewSet):
    pass
