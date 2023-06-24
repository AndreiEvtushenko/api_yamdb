from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api import views

v1_router = SimpleRouter()

v1_router.register('users', views.UserViewSet, basename='users')
v1_router.register(
    'categories', views.CategoriesViewSet, basename='сategories'
)
v1_router.register('titles', views.TitlesViewSet, basename='titles')
v1_router.register('genres', views.GenresViewSet, basename='genres')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewsViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentsViewSet,
    basename='comments'
)

urlpatterns = [
    path('users/me/', views.UserMeAPIView.as_view(
        {'get': 'retrieve', 'patch': 'partial_update'})),
    path('auth/signup/', views.SignUpView.as_view()),
    path('auth/token/', views.TokenView.as_view()),
    path('', include(v1_router.urls)),
]
