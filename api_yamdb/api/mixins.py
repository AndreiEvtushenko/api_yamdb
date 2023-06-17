from rest_framework import mixins, viewsets


class GetListCreateObject(mixins.CreateModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    pass


class GetListCreateRetrieveObject(mixins.CreateModelMixin,
                                  mixins.ListModelMixin,
                                  mixins.RetrieveModelMixin,
                                  viewsets.GenericViewSet):
    pass


class AuthorSaveMixins:
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
