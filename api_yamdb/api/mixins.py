from rest_framework import mixins, viewsets

from users.models import User


class GetListCreateDelObjectMixin(mixins.CreateModelMixin,
                                  mixins.ListModelMixin,
                                  mixins.DestroyModelMixin,
                                  viewsets.GenericViewSet):
    pass


class GetListCreateRetrieveObjectMixin(mixins.UpdateModelMixin,
                                       mixins.CreateModelMixin,
                                       mixins.ListModelMixin,
                                       mixins.RetrieveModelMixin,
                                       viewsets.GenericViewSet):
    pass


class AuthorSaveMixins:
    def perform_create(self, serializer):
        serializer.save(author=User.objects.get(username='admin'),
                        title_id=self.kwargs.get('title_id'))


class UserMeViewSetMixin(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    pass
