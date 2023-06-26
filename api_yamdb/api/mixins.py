from rest_framework import mixins, viewsets
from rest_framework import status
from rest_framework.response import Response

from .constants import NOT_FOUND_CATEGORY, NOT_FOUND_GENRE
from reviews.models import Categories, Genres


class GetListCreateDelObjectMixin(mixins.CreateModelMixin,
                                  mixins.ListModelMixin,
                                  mixins.DestroyModelMixin,
                                  viewsets.GenericViewSet):
    """Базовый класс для классов CategoriesViewSet и GenresViewSet"""

    pass


class UserMeViewSetMixin(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    """Базовый класс для класса UserMeAPIView"""

    pass


class DestroyMixin:
    """
    Класс для удаления объекта, применяется для
    классов CategoriesViewSet и GenresViewSet
    """

    def destroy(self, request, *args, **kwargs):
        if request.method == 'DELETE':
            slug = self.kwargs.get('pk')

            if self.__class__.__name__ == 'CategoriesViewSet':
                category = Categories.objects.filter(slug=slug)
                if category.exists():
                    category.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response(
                        data=NOT_FOUND_CATEGORY,
                        status=status.HTTP_404_NOT_FOUND
                    )

            elif self.__class__.__name__ == 'GenresViewSet':
                genres = Genres.objects.filter(slug=slug)
                if genres.exists():
                    genres.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response(
                        data=NOT_FOUND_GENRE,
                        status=status.HTTP_404_NOT_FOUND
                    )
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
