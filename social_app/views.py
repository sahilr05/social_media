from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from social_app import service
from social_app.models import User
# Create your views here.

class TestApi(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        return Response(data={"message": "Hello, world!"}, status=status.HTTP_200_OK)

class UserSignUp(APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()
        first_name = serializers.CharField()
        last_name = serializers.CharField()

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = "__all__"

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = service.user_signup(**serializer.validated_data)
        return Response(data=self.OutputSerializer(user).data, status=status.HTTP_201_CREATED)

    
class Follow(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        service.follow_user(user=request.user, follow_user_id=id)
        return Response(status=status.HTTP_201_CREATED)

class Unfollow(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        service.unfollow_user(user=request.user, unfollow_user_id=id)
        return Response(status=status.HTTP_204_NO_CONTENT)