from rest_framework import mixins, viewsets


class GetListCreateObjectDelObject(mixins.CreateModelMixin,
                                   mixins.ListModelMixin,
                                   mixins.DestroyModelMixin,
                                   viewsets.GenericViewSet):
    pass


class AuthorSaveMixins:
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
