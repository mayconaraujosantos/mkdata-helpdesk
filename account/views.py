from rest_framework import status, viewsets
from rest_framework.response import Response

from .serializers import UserSerializer

# Create your views here.


class UserListView(viewsets.ViewSet):
    @staticmethod
    # pylint: disable=unused-argument
    def create(request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
