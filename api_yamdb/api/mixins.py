from rest_framework import mixins, viewsets


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


class UserMeViewSetMixin(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    pass
