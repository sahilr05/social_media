from django.urls import path
from social_app import views


app_name="social_app"
urlpatterns = [
    path("test/", views.TestApi().as_view(), name="test_api"),
]
