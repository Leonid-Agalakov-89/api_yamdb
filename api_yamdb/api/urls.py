from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet, UserViewSet, signup, token)

API_VER_1_PREFIX = 'v1'

router_v_1 = DefaultRouter()
router_v_1.register(r'categories', CategoryViewSet)
router_v_1.register(r'genres', GenreViewSet)
router_v_1.register(r'titles', TitleViewSet)
router_v_1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews',
)
router_v_1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='reviews',
)
router_v_1.register(
    'users',
    UserViewSet,
    basename='users'
)

auth_urls = [
    path('token/', token, name='token'),
    path('signup/', signup, name='signup'),
]

urlpatterns = [
    path(f'{API_VER_1_PREFIX}/', include(router_v_1.urls)),
    path(f'{API_VER_1_PREFIX}/auth/', include(auth_urls)),
]
