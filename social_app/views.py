from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from social_app import service
from social_app.models import Comment
from social_app.models import Post
from social_app.models import User

# Create your views here.

# class TestApi(APIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request):
#         return Response(data={"message": "Hello, world!"}, status=status.HTTP_200_OK)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["comment_id", "message"]


class UserSignUpAPI(APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()
        first_name = serializers.CharField()
        last_name = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service.user_signup(**serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)


class UserDetailAPI(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = [
                "user_id",
                "email",
                "name",
                "username",
                "description",
                "following_count",
                "follower_count",
            ]

    def get(self, request):
        user = service.user_detail(user=request.user)
        response_data = self.OutputSerializer(user).data
        return Response(data=response_data, status=status.HTTP_200_OK)


class FollowAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        service.follow_user(user=request.user, follow_user_id=id)
        return Response(status=status.HTTP_201_CREATED)


class UnfollowAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        service.unfollow_user(user=request.user, unfollow_user_id=id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreatePostAPI(APIView):
    permission_classes = (IsAuthenticated,)

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField()
        description = serializers.CharField()

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            fields = [
                "post_id",
                "title",
                "description",
                "created_datetime",
            ]

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = service.create_post(user=request.user, **serializer.validated_data)
        response_data = self.OutputSerializer(post).data
        return Response(data=response_data, status=status.HTTP_201_CREATED)


class PostAPI(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        like_count = serializers.ReadOnlyField()
        comment_count = serializers.ReadOnlyField()

        class Meta:
            model = Post
            fields = "__all__"

    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        post = service.post_detail(user=request.user, post_id=id)
        response_data = self.OutputSerializer(post).data
        return Response(data=response_data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        service.delete_post(user=request.user, post_id=id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListPostAPI(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        like_count = serializers.ReadOnlyField()
        comments = CommentSerializer(many=True)

        class Meta:
            model = Post
            fields = [
                "post_id",
                "title",
                "description",
                "created_datetime",
                "comments",
                "like_count",
            ]

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        posts = service.list_post_by_user(user=request.user)
        response_data = self.OutputSerializer(posts, many=True).data
        return Response(data=response_data, status=status.HTTP_200_OK)


class LikePostAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        service.like_post(user=request.user, post_id=id)
        return Response(status=status.HTTP_201_CREATED)


class UnlikePostAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        service.unlike_post(user=request.user, post_id=id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddCommentAPI(APIView):
    class InputSerializer(serializers.Serializer):
        message = serializers.CharField()

    class OutputSerializer(serializers.Serializer):
        comment_id = serializers.UUIDField()

    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment_id = service.add_comment(
            user=request.user, post_id=id, **serializer.validated_data
        )
        response_data = self.OutputSerializer({"comment_id": comment_id}).data
        return Response(data=response_data, status=status.HTTP_201_CREATED)
