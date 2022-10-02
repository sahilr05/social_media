from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class TestApi(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        return Response(data={"message": "Hello, world!"}, status=status.HTTP_200_OK)