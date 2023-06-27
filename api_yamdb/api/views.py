from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404


from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .constants import (NOT_FOUND_USER_WITH_EMAIL,
                        NOT_FOUND_CATEGORY,
                        NOT_FOUND_GENRE)
from .permissions import (CommentReviewsPermission,
                          OnlyAdminOrSuperUserPermission,
                          SaveMethodsOrAdminPermission)
from .filters import TitlesFilter
from reviews.models import Categories, Comments, Genres, Title, Review
from .mixins import (DestroyMixin,
                     GetListCreateDelObjectMixin,
                     UserMeViewSetMixin)
from .serializers import (CategoriesSerializer, CommentsSerializer,
                          GenresSerializer, TokenSerializer,
                          TitlesCreateUpdateSerializer, TitlesSerializer,
                          ReviewsSerializer, SignupSerializer,
                          UserSerializer, UserMeSerializer)
from .utils.create_send_code import create_send_code

User = get_user_model()


class CategoriesViewSet(DestroyMixin, GetListCreateDelObjectMixin):
    """Вьюсет категорий"""

    queryset = Categories.objects.all().order_by('id')
    serializer_class = CategoriesSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    permission_classes = [SaveMethodsOrAdminPermission, ]

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, Categories, *args, **kwargs)

    def get_not_found_message(self):
        return NOT_FOUND_CATEGORY


class GenresViewSet(DestroyMixin, GetListCreateDelObjectMixin):
    """Вьюсет жанров"""

    queryset = Genres.objects.all().order_by('id')
    serializer_class = GenresSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    permission_classes = [SaveMethodsOrAdminPermission, ]

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, Genres, *args, **kwargs)

    def get_not_found_message(self):
        return NOT_FOUND_GENRE


class TitlesViewSet(viewsets.ModelViewSet):
    """Вьюсет произведений"""

    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = TitlesFilter
    search_fields = ('id', 'name',)
    pagination_class = PageNumberPagination
    permission_classes = [SaveMethodsOrAdminPermission, ]
    ordering_fields = ['name', 'year', 'genre', 'category']
    ordering = ['name']

    def get_serializer_class(self):
        """Возвращает необходимый сериализатор"""
        if self.request.method == 'GET':
            return TitlesSerializer

        elif self.request.method in ['POST', 'PATCH', 'DELETE']:
            return TitlesCreateUpdateSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    """Вьюсет отзывов"""

    serializer_class = ReviewsSerializer
    pagination_class = PageNumberPagination
    permission_classes = [CommentReviewsPermission, ]

    def get_queryset(self):
        title = self.kwargs.get('title_id')
        return Review.objects.filter(title=title).order_by('id')

    def perform_create(self, serializer):
        title = self.kwargs.get('title_id')

        title_object = get_object_or_404(Title, id=title)

        review_copy = Review.objects.filter(
            author=self.request.user, title=title_object
        )

        if review_copy:
            raise ValidationError('У вас уже есть отзыв у этого произведения')
        serializer.save(author=self.request.user, title=title_object)


class CommentsViewSet(viewsets.ModelViewSet):
    """Вьюсет комментариев"""

    serializer_class = CommentsSerializer
    pagination_class = PageNumberPagination
    permission_classes = [CommentReviewsPermission, ]

    def get_queryset(self):
        reviews_id = self.kwargs.get('review_id')
        queryset = Comments.objects.filter(reviews_id=reviews_id)
        return queryset

    def perform_create(self, serializer):

        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))

        serializer.save(author=self.request.user, reviews_id=review)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет пользователей"""

    queryset = User.objects.all().order_by('id')
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('username',)
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = [OnlyAdminOrSuperUserPermission, ]

    def retrieve(self, request, *args, **kwargs):
        username = self.kwargs.get('pk')

        user = get_object_or_404(User, username=username)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        username = self.kwargs.get('pk')

        user = get_object_or_404(User, username=username)
        serializer = self.get_serializer(
            user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        username = self.kwargs.get('pk')

        user = get_object_or_404(User, username=username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserMeAPIView(UserMeViewSetMixin):
    """Вьюсет пользователя для запроса /users/me/"""

    serializer_class = UserMeSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return self.request.user


class SignUpView(APIView):
    """Вью для регистарции пользователя"""

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        email = validated_data['email']
        username = validated_data['username']

        user = User.objects.filter(username=username, email=email)
        if not user:
            if User.objects.filter(email=email).exists():
                return Response(
                    NOT_FOUND_USER_WITH_EMAIL,
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif User.objects.filter(username=username).exists():
                return Response(
                    NOT_FOUND_USER_WITH_EMAIL,
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                user = User.objects.create(username=username,
                                           email=email)
                create_send_code(user, username, email)
                return Response(serializer.data, status=status.HTTP_200_OK)

        create_send_code(user.first(), username, email)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(APIView):
    """Вью для получениятокена пользователя"""

    def post(self, request):
        serializer = TokenSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            username = validated_data['username']
            confirmation_code = validated_data['confirmation_code']

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response(
                    {'message': 'Пользователь не найден'},
                    status=status.HTTP_404_NOT_FOUND
                )

            if user.confirmation_code != confirmation_code:
                return Response(
                    {'message': 'Неверный код подтверждения'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = AccessToken.for_user(user)
            return Response(
                {'token': str(token)},
                status=status.HTTP_200_OK
            )

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
