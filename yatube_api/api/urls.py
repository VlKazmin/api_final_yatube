from django.urls import include, path

from rest_framework import routers

from api.views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

app_name = "api"

router_v1 = routers.DefaultRouter()

router_v1.register(r"posts", PostViewSet, basename="posts")
router_v1.register(r"groups", GroupViewSet, basename="groups")
router_v1.register(r"follow", FollowViewSet, basename="follow")
router_v1.register(
    r"^posts/(?P<post_id>\d+)/comments", CommentViewSet, basename="comments"
)

urlpatterns = [
    path("", include(router_v1.urls)),
    path("", include("djoser.urls.jwt")),
]
