from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api import views

router1 = SimpleRouter()

router1.register('users', views.UserViewSet, basename='users')
router1.register('categories', views.CategoriesViewSet, basename='сategories')
router1.register('titles', views.TitlesViewSet, basename='titles')
router1.register('genres', views.GenresViewSet, basename='genres')

router1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewsViewSet,
    basename='reviews'
)
router1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentsViewSet,
    basename='comments'
)

urlpatterns = [
    path('api/v1/users/me/', views.UserMeAPIView.as_view(
        {'get': 'retrieve', 'patch': 'partial_update'})),
    path('api/v1/auth/signup/', views.SignUpView.as_view()),
    path('api/v1/auth/token/', views.TokenView.as_view()),
    path('api/v1/', include(router1.urls)),
]
