from django.contrib.auth import get_user_model

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import (CommentReviewsPermission,
                          OnlyAdminOrSuperUserPermission,
                          SaveMethodsOrAdminPermission)
from reviews.models import Categories, Comments, Genres, Titles, Reviews
from .mixins import GetListCreateDelObjectMixin, UserMeViewSetMixin
from .serializers import (CategoriesSerializer, CommentsSerializer,
                          TitlesCreateUpdateSerializer,
                          GenresSerializer, TitlesSerializer,
                          ReviewsSerializer, UserSerializer,
                          UserMeSerializer)
from .utils.code_utils import create_verification_code
from .utils.email_utils import send_code

User = get_user_model()


class CategoriesViewSet(GetListCreateDelObjectMixin):
    """Вьюсет категорий"""
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination
    permission_classes = [SaveMethodsOrAdminPermission, ]

    def destroy(self, request, *args, **kwargs):
        if request.method == 'DELETE':
            slug_categories = self.kwargs.get('pk')
            try:
                categories = Categories.objects.get(slug=slug_categories)
                categories.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Categories.DoesNotExist:
                return Response(
                    data="Категория не найден",
                    status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenresViewSet(GetListCreateDelObjectMixin):
    """Вьюсет жанров"""
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination
    permission_classes = [SaveMethodsOrAdminPermission, ]

    def destroy(self, request, *args, **kwargs):
        if request.method == 'DELETE':
            slug_genres = self.kwargs.get('pk')
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
    """Вьюсет произведений"""
    queryset = Titles.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('name', 'year', 'description', 'genre', 'category')
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination
    permission_classes = [SaveMethodsOrAdminPermission, ]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitlesSerializer
        elif self.request.method in ['POST', 'PUT', 'PATCH']:
            return TitlesCreateUpdateSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    """Вьюсет отзывов"""
    serializer_class = ReviewsSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [CommentReviewsPermission, ]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        queryset = Reviews.objects.filter(title_id=title_id)
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title_object = Titles.objects.get(id=title_id)
        if title_object is None:
            raise ValidationError('Bad')
        serializer.save(
            author=User.objects.get(username='admin'), title_id=title_object)


class CommentsViewSet(viewsets.ModelViewSet):
    """Вьюсет комментариев"""
    serializer_class = CommentsSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [CommentReviewsPermission, ]

    def get_queryset(self):
        reviews_id = self.kwargs.get('review_id')
        queryset = Comments.objects.filter(reviews_id=reviews_id)
        return queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review_id_object = Reviews.objects.get(id=review_id)
        if review_id_object is None:
            raise ValidationError('Bad')
        serializer.save(
            author=User.objects.get(username='admin'),
            reviews_id=review_id_object)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет пользователей"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [OnlyAdminOrSuperUserPermission, ]

    def retrieve(self, request, *args, **kwargs):
        username = self.kwargs.get('pk')
        try:
            user = User.objects.get(username=username)
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                data="Пользователь не найден",
                status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, *args, **kwargs):
        username = self.kwargs.get('pk')
        try:
            user = User.objects.get(username=username)
            serializer = self.get_serializer(
                user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                data="Пользователь не найден",
                status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        username = self.kwargs.get('pk')
        try:
            user = User.objects.get(username=username)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(
                data="Пользователь не найден",
                status=status.HTTP_404_NOT_FOUND)


class UserMeAPIView(UserMeViewSetMixin):
    serializer_class = UserMeSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return self.request.user


class SignUpView(APIView):

    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        confirmation_code = create_verification_code()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response('Пользователь с указанным именем не существует',
                            status=status.HTTP_400_BAD_REQUEST)
        user.confirmation_code = confirmation_code
        user.save()
        send_code(email, confirmation_code, username)
        data = {
            'email': email,
            'username': username
        }
        return Response(data, status=status.HTTP_200_OK)


class TokenView(APIView):

    def post(self, request):
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')
        user = User.objects.get(username=username)
        if user.confirmation_code == confirmation_code:
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Неверный код подтверждения'},
                            status=status.HTTP_400_BAD_REQUEST)
