from rest_framework import mixins, viewsets
from rest_framework import status
from rest_framework.response import Response


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

    def destroy(self, request, model, *args, **kwargs):
        if request.method == 'DELETE':
            slug = self.kwargs.get('pk')

            obj = model.objects.filter(slug=slug)
            if obj.exists():
                obj.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    data=self.get_not_found_message(),
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_not_found_message(self):
        """Метод для получения сообщения об объекте не найден"""
        raise NotImplementedError(
            'Метод "get_not_found_message"'
            'необходимо реализовать в дочерних классах.'
        )
