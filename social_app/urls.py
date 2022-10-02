from django.urls import path
from social_app import views


app_name="social_app"
urlpatterns = [
    path("test/", views.TestApi().as_view(), name="test_api"),
    path("user/sign_up/", views.UserSignUp().as_view(), name="user_sign_up"),
    path("follow/<uuid:id>/", views.Follow().as_view(), name="follow"),
    path("unfollow/<uuid:id>/", views.Unfollow().as_view(), name="follow"),
]
