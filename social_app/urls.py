from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from social_app import views

app_name = "social_app"
urlpatterns = []

user_urls = [
    # path("test/", views.TestApi().as_view(), name="test_api"),
    path(
        "authentication/",
        jwt_views.TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("user/", views.UserDetailAPI().as_view(), name="user_detail"),
    path("user/sign_up/", views.UserSignUpAPI().as_view(), name="user_sign_up"),
]

follow_urls = [
    path("follow/<uuid:id>/", views.FollowAPI().as_view(), name="follow"),
    path("unfollow/<uuid:id>/", views.UnfollowAPI().as_view(), name="follow"),
]

post_urls = [
    path("all_posts/", views.ListPostAPI().as_view(), name="user_posts"),
    path("posts/", views.CreatePostAPI().as_view(), name="create_post"),
    path("posts/<uuid:id>/", views.PostAPI().as_view(), name="post"),
    path("like/<uuid:id>/", views.LikePostAPI().as_view(), name="like_post"),
    path("unlike/<uuid:id>/", views.UnlikePostAPI().as_view(), name="unlike_post"),
    path("comment/<uuid:id>/", views.AddCommentAPI().as_view(), name="add_comment"),
]

urlpatterns.extend(user_urls + follow_urls + post_urls)
